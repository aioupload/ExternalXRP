#tejask@mit.edu - MIT Probabilistic Computing Group

import pdb
import scipy
import os, sys
from scipy import stats
from scipy import special

lib_path = os.path.abspath('ProbabilisticEngineTestSuite')
sys.path.append(lib_path)

import client
import lisp_parser # From here: http://norvig.com/lispy.html
import venture_infrastructure
from itertools import *
import openGLText
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import pylab
import Image
from numpy import *

RES = 200*200

class stochastic_test(venture_infrastructure.venture_infrastructure):

  def initPlottingHarness(self,baselineIm,im,X,logsArray,pxdisagree,pflip,blur,cnt):
    self.f = pylab.figure()

    self.f.subplots_adjust(hspace=0.5)

    self.f.add_subplot(321,title='Original Image')
    pylab.imshow(baselineIm)

    self.f.add_subplot(322,title='Inferred Image')
    pylab.imshow(im)

    self.f.add_subplot(323,title='Logscore')
    pyplot.plot( X, logsArray, '-' )
    pyplot.xlabel( 'Iterations' )
    pyplot.ylabel( 'Logscore' )

    #pxdisagree
    self.f.add_subplot(324,title='PX DIFF')
    pyplot.plot( X, pxdisagree, '-' )
    pyplot.xlabel( 'Iterations' )
    pyplot.ylabel( 'px_disagree' )


    self.f.add_subplot(325,title='PFLIP')
    pyplot.plot( X, pflip, '-' )
    pyplot.xlabel( 'Iterations' )
    pyplot.ylabel( 'PFLIP' )

    self.f.add_subplot(326,title='Blur')
    pyplot.plot( X, blur, '-' )
    pyplot.xlabel( 'Iterations' )
    pyplot.ylabel( 'Blur' )

    pylab.savefig('dump/test'+str(cnt)+'.png')



  def LoadProgram(self):
    MyRIPL = self.RIPL
    
    MyRIPL.clear() # To delete previous sessions data.
   
    (_posx, tmp) = MyRIPL.assume("posx", lisp_parser.parse("(uniform-discrete 20 180)"))
    (_posy, tmp) = MyRIPL.assume("posy", lisp_parser.parse("(uniform-discrete 20 180)"))
    (_size, tmp) = MyRIPL.assume("size", lisp_parser.parse("(uniform-discrete 20 50)"))
    (_id_directive, tmp) =  MyRIPL.assume("id", lisp_parser.parse("(uniform-discrete 0 25)"))
    
    #(_blur, tmp) = MyRIPL.assume("blur", lisp_parser.parse("(* (beta 1 6) 40)"))
    (_blur, tmp) = MyRIPL.assume("blur", lisp_parser.parse("0"))
    #(_blur, tmp) = MyRIPL.assume("blur", lisp_parser.parse("(uniform-continuous 0.0 10.0)"))
    

    (_alpha,tmp)= MyRIPL.assume("alpha", lisp_parser.parse("(uniform-continuous 0.01 8)"))    
    
    #Original :(_pflip,tmp)= MyRIPL.assume("pflip", lisp_parser.parse("(beta 1 alpha)"))
    
    #3choices
    #MyRIPL.assume("pflipHelper", lisp_parser.parse("(uniform-discrete 0 2)"))
    #(_pflip,tmp)= MyRIPL.assume("pflip", lisp_parser.parse("(if (= pflipHelper 0) 0.1 (if (= pflipHelper 1) 0.2 0.7) )"))
    
    (_pflip,tmp)= MyRIPL.assume("pflip", lisp_parser.parse("(uniform-continuous 0.0 1.0)"))


    MyRIPL.assume("LOAD-IMAGE", lisp_parser.parse("1"))
    MyRIPL.assume("RENDER-IMAGE", lisp_parser.parse("10"))
    MyRIPL.assume("NOISY-COMP", lisp_parser.parse("3"))

    MyRIPL.assume("load-image", lisp_parser.parse("(load-remote-xrp 4444 LOAD-IMAGE)"))    
    MyRIPL.assume("render-image", lisp_parser.parse("(load-remote-xrp 4444 RENDER-IMAGE)"))    
    MyRIPL.assume("noisy-image-compare", lisp_parser.parse("(load-remote-xrp 4444 NOISY-COMP)"))    

    MyRIPL.assume("test-image", lisp_parser.parse("(load-image 0 0 0 0 0)")) #FIXME - dynamic args
    MyRIPL.assume("rendered-image", lisp_parser.parse("(render-image posx posy id size blur)")) #FIXME - dynamic args

    MyRIPL.observe(lisp_parser.parse("(noisy-image-compare test-image rendered-image pflip)"), "true")

    r = openGLText.openGLText()

    logsArray = []
    pxdisagreeArr = []
    blurArr = []
    pflipArr = []
    baselineIm = Image.open("demo.jpg").convert("L")
    baselineIm = asarray(baselineIm)

    cnt = 0
    while cnt < 200:
        MyRIPL.infer(100)
        posx = MyRIPL.report_value(_posx)
        posy = MyRIPL.report_value(_posy)
        size = MyRIPL.report_value(_size)
        _id = MyRIPL.report_value(_id_directive)
        blur = MyRIPL.report_value(_blur)
        alpha = MyRIPL.report_value(_alpha)
        pflip = MyRIPL.report_value(_pflip)


        print "left(120):",posx," top(90):", posy," size(30):", size,chr(_id+65)," blur: ",blur, "| alpha:", alpha,"| pflip:", pflip

        things = []
        things.append({'id':chr(int(_id)+65), 'size':size, 'left':posx, 'top':posy,'blur_sigsq':blur})
        im = r.get_rendered_image(things)
        scipy.misc.imsave('inference.jpg', im)
        logscore = MyRIPL.logscore()
        logsArray.append(logscore['logscore'])

        compound = im+baselineIm
        intersection_ones = len(where(compound == 2)[0])
        intersection_zeros = len(where(compound == 0)[0])
        intersection = intersection_zeros + intersection_ones
        pxdisagreeArr.append(float(RES-intersection)/RES)

        pflipArr.append(pflip)
        blurArr.append(blur)

        print 'LOGSCORE:', logscore, "|", cnt
        cnt = cnt + 1

        self.initPlottingHarness(baselineIm,im,range(cnt),logsArray,pxdisagreeArr,pflipArr,blurArr,cnt)



    """ # add directives needed
    directives=list()
    directives.append(last_directive)

    self.directives = directives"""


  def __init__(self):
    import os.path
    self.name = os.path.basename(__file__)
    self.description = "TBA."
  

rd=stochastic_test()
Port = 8082
rd.RIPL = client.RemoteRIPL("http://127.0.0.1:" + str(Port))
rd.LoadProgram()

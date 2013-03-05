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
import matplotlib.cm as cm


RES = 200*200
MAX_LETTERS = 3

class stochastic_test(venture_infrastructure.venture_infrastructure):



  def demoPlotting(self,baselineIm,im,X,logsArray,pxdisagree,pflip,blur,cnt):
    self.f = pylab.figure()

    self.f.add_subplot(121,title='Original Image')
    pylab.imshow(baselineIm,cmap=pyplot.cm.binary)

    self.f.add_subplot(122,title='Inferred Image')
    pylab.imshow(im,cmap=pyplot.cm.binary)
    pylab.savefig('demo/test'+str(cnt)+'.png')




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


  def predictCharacteres(self):
    chrs = dict()  
    for i in range(MAX_LETTERS):
        chrs[i]={'posx':None};chrs[i]={'posy':None};chrs[i]={'size':None};chrs[i]={'id':None};chrs[i]={'blur':None}; chrs[i]={'present':None};
        (chrs[i]['posx'], _) = self.RIPL.predict(lisp_parser.parse('(posx '+str(i)+')'))
        (chrs[i]['posy'], _) = self.RIPL.predict(lisp_parser.parse('(posy '+str(i)+')'))
        (chrs[i]['size'], _) = self.RIPL.predict(lisp_parser.parse('(size '+str(i)+')'))
        (chrs[i]['id'], _) = self.RIPL.predict(lisp_parser.parse('(id '+str(i)+')'))
        (chrs[i]['blur'], _) = self.RIPL.predict(lisp_parser.parse('(blur '+str(i)+')'))
        (chrs[i]['present'], _) = self.RIPL.predict(lisp_parser.parse('(letter-present '+str(i)+')'))
    return chrs

  def reportCharacters(self,chrs,i):
    posx = self.RIPL.report_value(chrs[i]['posx'])
    posy = self.RIPL.report_value(chrs[i]['posy'])
    size = self.RIPL.report_value(chrs[i]['size'])
    _id = self.RIPL.report_value(chrs[i]['id'])
    blur = self.RIPL.report_value(chrs[i]['blur'])
    present = self.RIPL.report_value(chrs[i]['present'])
    return posx,posy,size,_id,blur,present


  def LoadProgram(self):
    MyRIPL = self.RIPL
    
    MyRIPL.clear() # To delete previous sessions data.

    MyRIPL.assume("letter-present", lisp_parser.parse("(mem (lambda(letter-id) (bernoulli 1.0)))"))
    
    self.RIPL.assume("posx", lisp_parser.parse("(mem (lambda (letter-id) (uniform-discrete 0 150)))")) #0 -140 captcha
    self.RIPL.assume("posy", lisp_parser.parse("(mem (lambda (letter-id) (uniform-discrete 0 150)))")) #0 - 100 captcha #56-64 ocr
    self.RIPL.assume("size", lisp_parser.parse("(mem (lambda (letter-id) (uniform-discrete 30 70)))")) #30-70 captcha
    self.RIPL.assume("id", lisp_parser.parse("(mem (lambda (letter-id) (uniform-discrete 0 2)))")) #0 -2
    self.RIPL.assume("blur", lisp_parser.parse("(mem (lambda (letter-id) (uniform-continuous 0.0 20.0)))")) # 0 - 10

    (_alpha,tmp) = MyRIPL.assume("alpha", lisp_parser.parse("(uniform-continuous 0 20)"))
    (_pflip,tmp)= MyRIPL.assume("pflip", lisp_parser.parse("(beta 6 6)"))


    MyRIPL.assume("LOAD-IMAGE", lisp_parser.parse("1"))
    MyRIPL.assume("RENDER-IMAGE", lisp_parser.parse("10"))
    MyRIPL.assume("NOISY-COMP", lisp_parser.parse("3"))

    MyRIPL.assume("load-image", lisp_parser.parse("(load-remote-xrp 4444 LOAD-IMAGE)"))    
    MyRIPL.assume("render-image", lisp_parser.parse("(load-remote-xrp 4444 RENDER-IMAGE)"))    
    MyRIPL.assume("noisy-image-compare", lisp_parser.parse("(load-remote-xrp 4444 NOISY-COMP)"))    

    MyRIPL.assume("test-image", lisp_parser.parse("(load-image 0 0 0 0 0)")) #FIXME - dynamic args
    
    arguments = ""
    for i in range(MAX_LETTERS):
        arguments += " (posx "+str(i)+") " + " (posy "+str(i)+") " + " (id "+str(i)+") " + " (size "+str(i)+") " + " (blur "+str(i)+") " + " (letter-present "+str(i)+") "
    

    MyRIPL.assume("rendered-image", lisp_parser.parse("(render-image " + arguments + ")")) #FIXME - dynamic args

    MyRIPL.observe(lisp_parser.parse("(noisy-image-compare test-image rendered-image pflip)"), "true")

    r = openGLText.openGLText()

    logsArray = []
    pxdisagreeArr = []
    blurArr = []
    pflipArr = []
    baselineIm = Image.open("demo.jpg").convert("L")
    baselineIm = asarray(baselineIm)

    chrs = self.predictCharacteres()

    cnt = 0
    while cnt < 200:
        MyRIPL.infer(50)

        pflip = MyRIPL.report_value(_pflip)
        things = []

        for i in range(MAX_LETTERS):
            posx,posy,size,_id,blur,present = self.reportCharacters(chrs,i)
            print present
            if present == True:
                things.append({'id':chr(int(_id)+65), 'size':size, 'left':posx, 'top':posy,'blur_sigsq':blur})
                print "left():",posx," top():", posy," size():", size,chr(_id+65)," blur: ",blur,"| pflip:", pflip
        print "####\n"

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
        #self.demoPlotting(baselineIm,im,range(cnt),logsArray,pxdisagreeArr,pflipArr,blurArr,cnt)


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

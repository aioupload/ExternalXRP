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
import Renderer
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages


class stochastic_test(venture_infrastructure.venture_infrastructure):

  def LoadProgram(self):
    MyRIPL = self.RIPL
    
    MyRIPL.clear() # To delete previous sessions data.
   
    MyRIPL.assume("posx", lisp_parser.parse("(uniform-discrete 0 180)"))
    MyRIPL.assume("posy", lisp_parser.parse("(uniform-discrete 0 180)"))
    MyRIPL.assume("size", lisp_parser.parse("(uniform-discrete 30 60)"))
    MyRIPL.assume("id", lisp_parser.parse("(uniform-discrete 0 25)"))
    MyRIPL.assume("blur", lisp_parser.parse("(* (beta 1 0.9) 40)"))
    MyRIPL.assume("alpha", lisp_parser.parse("(uniform-continuous 0.01 8)"))    
    MyRIPL.assume("pflip", lisp_parser.parse("(beta 1 alpha)"))

    MyRIPL.assume("LOAD-IMAGE", lisp_parser.parse("1"))
    MyRIPL.assume("RENDER-IMAGE", lisp_parser.parse("10"))
    MyRIPL.assume("NOISY-COMP", lisp_parser.parse("3"))

    MyRIPL.assume("load-image", lisp_parser.parse("(load-remote-xrp 4444 LOAD-IMAGE)"))    
    MyRIPL.assume("render-image", lisp_parser.parse("(load-remote-xrp 4444 RENDER-IMAGE)"))    
    MyRIPL.assume("noisy-image-compare", lisp_parser.parse("(load-remote-xrp 4444 NOISY-COMP)"))    

    MyRIPL.assume("test-image", lisp_parser.parse("(load-image 0 0 0 0 0)")) #FIXME - dynamic args
    MyRIPL.assume("rendered-image", lisp_parser.parse("(render-image posx posy id size blur)")) #FIXME - dynamic args

    MyRIPL.observe(lisp_parser.parse("(noisy-image-compare test-image rendered-image pflip)"), "true")

    r = Renderer.Renderer()
    r.state = dict()
    r.state['params'] = {'room_self.size_x':r.size_x, 'room_self.size_y':r.size_y}
    r.state['blur'] = True

    logsArray = []
    cnt = 0
    while cnt < 600:
        MyRIPL.infer(50)
        posx = MyRIPL.report_value(1)
        posy = MyRIPL.report_value(2)
        size = MyRIPL.report_value(3)
        _id  = MyRIPL.report_value(4)
        blur = MyRIPL.report_value(5)
        alpha = MyRIPL.report_value(6)
        pflip = MyRIPL.report_value(7)
        print posx,posy,size,chr(_id+65),blur, "| alpha:", alpha,"| pflip:", pflip

        things = []
        things.append({'id':chr(int(_id)+65), 'size':size, 'left':posx, 'top':posy,'blur_sigsq':blur})
        im = r.get_rendered_image(things)
        scipy.misc.imsave('inference.jpg', im)
        logscore = MyRIPL.logscore()
        logsArray.append(logscore['logscore'])
        print 'LOGSCORE:', logscore, "|", cnt
        cnt = cnt + 1

    X = range(cnt)
    pyplot.plot( X, logsArray, '-' )
    pyplot.xlabel( 'Iterations' )
    pyplot.ylabel( 'Logscore' )
    pyplot.savefig( 'Simple.png' )
    pyplot.show()

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

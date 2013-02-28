#tejask@mit.edu - MIT Probabilistic Programming Group
#Inverse Graphics - Rendering driver for Toyota driverless car data

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import pygame, pygame.image
from pygame.locals import *
import pickle
from numpy import *
import os
import pdb
import numpy as np
import glFreeType 
from math import cos
import time 
import pylab
from scipy.ndimage.filters import *
import numpy.random as npr
import scipy
import pylab
from matplotlib import pyplot


width,height = (200,200)
SIZEX = width
SIZEY = height
REFLECTANCE_THRESHOLD = 0
FONT_SIZE = 100

class openGLText:
    def __init__(self):
        pygame.init()
        WINDOW = pygame.display.set_mode((width,height),OPENGL|DOUBLEBUF)
        pygame.display.set_caption('3D Text Renderer')
        glutInit(sys.argv)
        self.WINDOW = WINDOW
        self.our_font = glFreeType.font_data("Test.ttf", FONT_SIZE)

        self.loglikelihood = None
        self.observedIm = None
        self.currentIm = None
        self.state = dict()
        self.state['params'] = {'room_self.size_x':SIZEX, 'room_self.size_y':SIZEY}
        self.state['blur'] = True
        self.resolution = SIZEX*SIZEY

        self.pool = dict()



    def loadImage(self,filename):
        self.observedIm = pickle.load(open("demo.pkl","rb")) #Image.load('filename')
        return 1



    def getLogLikelihood(self,imageid,pflip):
        if self.pool.has_key(imageid):
            intersection = self.pool[imageid]['intersection']
        else:
            compound = self.currentIm+self.observedIm
            intersection_ones = len(np.where(compound == 2)[0])
            intersection_zeros = len(np.where(compound == 0)[0])
            intersection = intersection_zeros + intersection_ones
            self.pool[imageid] = {'intersection':intersection}

        self.loglikelihood = intersection*log(1-pflip) + (self.resolution - intersection)*log(pflip)
        #print pflip, self.loglikelihood, intersection, self.resolution 

        return self.loglikelihood



    def OLDgetLogLikelihood(self,pflip):
        compound = self.currentIm+self.observedIm
        intersection_ones = len(np.where(compound == 2)[0])
        intersection_zeros = len(np.where(compound == 0)[0])
        intersection = intersection_zeros + intersection_ones
        self.loglikelihood = intersection*log(1-pflip) + (self.resolution - intersection)*log(pflip)
        #print pflip, self.loglikelihood, intersection, self.resolution
            
        return self.loglikelihood

    def makeGraph(self,fname):
        f = pylab.figure()
        bin = []
        X = []
        drange = arange(0.05,1.0,0.05)
        CNT = 0
        for i in drange:
            X.append(CNT)
            L = self.getLogLikelihood(i)
            bin.append(L)
            CNT += 1

        pdb.set_trace()
        #Normalizing
        m = max(bin)
        bin -= log(sum(exp(bin-m))) + m
        bin = exp(bin)

        f.add_subplot(111,title='Marginal')
        pyplot.plot( X, bin, '-' )
        pyplot.xlabel( 'Support' )
        pyplot.ylabel( 'Probability' )
        pylab.savefig(fname)


    def testPFLIP(self):
        glViewport(0,0,width,height)

        things = []
        things.append({'id':'C', 'size':30, 'left':120, 'top':90,'blur_sigsq':0})
        im = self.get_rendered_image(things)
        self.observedIm = im

        things = []
        things.append({'id':'C', 'size':30, 'left':120, 'top':90,'blur_sigsq':0})
        im = self.get_rendered_image(things)
        self.currentIm = im
        self.makeGraph("overlap.png")

        things = []
        things.append({'id':'C', 'size':30, 'left':30, 'top':30,'blur_sigsq':0})
        im = self.get_rendered_image(things)
        self.currentIm = im
        self.makeGraph("NONoverlap.png")



    def convSurfaceToImg(self,BLUR):
        im_str = pygame.image.tostring(self.WINDOW,'RGB')
        a = np.fromstring(im_str, dtype=np.uint8)
        bim = a.reshape(SIZEX,SIZEY, 3)
        bim = np.sum(bim, 2)
        bim = np.float64(bim)
        bim = bim/np.max(bim)
        if BLUR > 0:
            bim = gaussian_filter(bim, BLUR, mode='wrap')
            bim = npr.binomial(1, bim/np.max(bim))
        return bim


    def get_rendered_image(self,things):
        for i in range(len(things)):
            self.drawText(things[i])
            bim = self.convSurfaceToImg(things[i]['blur_sigsq'])
            if i == 0:
                bim[bim.nonzero()] = 1
                im = bim
            else:
                im[bim.nonzero()] = 1
            pygame.display.flip()
        #scipy.misc.imsave('all.jpg', im)
        self.currentIm = im
        return im

    def drawText(self,thing):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPushMatrix();
        glEnable(GL_DEPTH_TEST)
        glClear(GL_DEPTH_BUFFER_BIT) 
        scaling = float(thing['size'])/FONT_SIZE 
        glScalef(scaling,scaling,1)
        self.our_font.glPrint (thing['left'],thing['top'],thing['id'])
        glPopMatrix()

    def sample_from_prior(self):
        glViewport(0,0,width,height)
        things = []
        #things.append({'id':'C', 'size':70, 'left':20, 'top':50,'blur_sigsq':2})
        things.append({'id':'D', 'size':50, 'left':55, 'top':70,'blur_sigsq':1.3})
        things.append({'id':'E', 'size':45, 'left':80, 'top':60,'blur_sigsq':0})
        things.append({'id':'A', 'size':60, 'left':100, 'top':75,'blur_sigsq':1.2})
        things.append({'id':'B', 'size':50, 'left':120, 'top':65,'blur_sigsq':0.6})
        t1=time.time()
        im = self.get_rendered_image(things)

        for ii in range(width):
            for jj in range(height):
                if np.random.binomial(1,0.01) is 1:
                    im[ii][jj] = 1

        pickle.dump(im,open("demo.pkl","wb"))
        scipy.misc.imsave('demo.jpg', im)
        t2=time.time()
        print t2-t1

#r=openGLText()
#r.sample_from_prior()
#r.testPFLIP()


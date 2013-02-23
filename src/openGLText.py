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


width,height = (200,200)
SIZEX = width
SIZEY = height
REFLECTANCE_THRESHOLD = 0
FONT_SIZE = 30

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

    def loadImage(self,filename):
        self.observedIm = pickle.load(open("demo.pkl","rb")) #Image.load('filename')
        return 1

    def getLogLikelihood(self,pflip):
        compound = self.currentIm+self.observedIm
        intersection_ones = len(np.where(compound == 2)[0])
        intersection_zeros = len(np.where(compound == 0)[0])
        intersection = intersection_zeros + intersection_ones
        self.loglikelihood = intersection*log(1-pflip) + (self.resolution - intersection)*log(pflip)
        return self.loglikelihood


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
        things.append({'id':'C', 'size':60, 'left':120, 'top':90,'blur_sigsq':0})
        t1=time.time()
        im = self.get_rendered_image(things)
        pickle.dump(im,open("demo.pkl","wb"))
        scipy.misc.imsave('demo.jpg', im)
        t2=time.time()
        print t2-t1


#r=openGLText()
#r.sample_from_prior()


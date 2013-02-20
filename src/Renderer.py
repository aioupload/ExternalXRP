import numpy as np
from matplotlib import *
import matplotlib.cm as cm
from matplotlib.backends.backend_agg import FigureCanvasAgg 
from matplotlib.figure import Figure
from scipy.ndimage.filters import *
import time
import pdb
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr
from random import choice
import time
from matplotlib.pyplot import *
import pickle
from math import *
import scipy
import pdb
import pygame


SIZEX = 200
SIZEY = 200

class Renderer:

	def __init__(self):
		self.size_x, self.size_y = SIZEX, SIZEY
		self.my_dpi = 100
		self.inches_sizex, self.inches_sizey = self.size_x/self.my_dpi, self.size_y/self.my_dpi
		self.FLAG = 0

		#Important parameters
		self.loglikelihood = None
		self.observedIm = None
		self.currentIm = None
		self.state = dict()
		self.state['params'] = {'room_self.size_x':SIZEX, 'room_self.size_y':SIZEY}
		self.state['blur'] = True
		self.resolution = SIZEX*SIZEY
		#pygame.init()
		#self.screen = pygame.display.set_mode((SIZEX,SIZEY)) 


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

		""" works - funny 
		compound = self.currentIm+self.observedIm
		union = len(np.where(compound >= 1)[0])
		intersection = len(np.where(compound == 2)[0])
		self.loglikelihood = 10*log(float(intersection+1)/union)
		return self.loglikelihood"""

		""" slow version
		intersection = 0
		union = 0
		for ii in range(200):
			for jj in range(200):
				if self.observedIm[ii][jj] == 1 and self.currentIm[ii][jj] == 1:
					intersection = intersection + 1
				if self.observedIm[ii][jj] == 1 or self.currentIm[ii][jj] == 1:
					union = union + 1

		self.loglikelihood = log(float(intersection+1)/union)
		return self.loglikelihood"""


	def render_thing(self,thing):
		self.f = Figure(frameon=False, dpi=self.my_dpi)
		self.f.set_size_inches(self.inches_sizex, self.inches_sizey)	
		self.ax = Axes(self.f, [0., 0., 1., 1.])
		self.ax.set_axis_off()
		self.f.add_axes(self.ax)
		self.canvas = FigureCanvasAgg(self.f)

		self.ax.text(float(thing['left'])/self.state['params']['room_self.size_x'], float(thing['top'])/self.state['params']['room_self.size_y'], thing['id'], size = thing['size'])
		self.canvas.draw()

	 	im_str = self.canvas.tostring_rgb()
		a = np.fromstring(im_str, dtype=np.uint8)
	 	im = a.reshape(self.size_x, self.size_y, 3)

	   	im = np.sum(im, 2)
	   	im = np.float64(im)
	   	im = im/np.max(im)
	   	im = 1-im
	   	if self.state['blur']:
	   		bim = gaussian_filter(im, thing['blur_sigsq'], mode='wrap')
	   	return bim

	def get_rendered_image(self,things):
		#print things

		for i in range(len(things)):
			bim = self.render_thing(things[i])			
			bim = npr.binomial(1, bim/np.max(bim))
			if i == 0:
				bim[bim.nonzero()] = 1
				im = bim
			else:
				im[bim.nonzero()] = 1
		self.currentIm = im
		
		scipy.misc.imsave('output.jpg', im)

		return im


	def test(self):
		self.state = dict()
		self.state['params'] = {'room_self.size_x':SIZEX, 'room_self.size_y':SIZEY}
		self.state['blur'] = True

		things = []
		things.append({'id':'C', 'size':50, 'left':120, 'top':90,'blur_sigsq':0})
		#things.append({'id':'Z', 'size':20, 'left':0, 'top':100,'blur_sigsq':10})
		#things.append({'id':'C', 'size':30, 'left':40, 'top':120,'blur_sigsq':0})
		#things.append({'id':'E', 'size':50, 'left':140, 'top':160,'blur_sigsq':3})
		#things.append({'id':'M', 'size':20, 'left':240, 'top':20,'blur_sigsq':0})
	
		t0 = time.time()
		self.currentIm = self.get_rendered_image(things)
		t1 = time.time()
		print t1-t0
		pickle.dump(self.currentIm,open("demo.pkl","wb"))
		scipy.misc.imsave('demo.jpg', self.currentIm)
		"""scipy.misc.imsave('test1.jpg', self.currentIm)

		#imshow(im, cmap=cm.Greys)

		self.observedIm = pickle.load(open("demo.pkl","rb")) #Image.load('filename')
		scipy.misc.imsave('test2.jpg', self.observedIm)
		print "loglikelihood:", self.getLogLikelihood()"""


def runall():
	r = Renderer()
	r.test()


#runall()


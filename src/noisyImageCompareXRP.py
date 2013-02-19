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



class noisyImageCompareXRP:
	def __init__(self,renderer):
		self.id_of_this_xrp = 3
		self.is_scorable = 1
		self.is_random_choice = 1
		self.name = "noisyImageCompareXRP"
		self.renderer = renderer
		self.logl = dict()

	def execFunc(self,args):
		return

	def getLogLikelihood(self,imageid,pflip):
		if (self.logl.has_key(imageid)):
			#print imageid, "||", self.logl[imageid]
			return self.logl[imageid]
		else:
			l = self.renderer.getLogLikelihood(pflip)
			self.logl[imageid] = l
			#print imageid, "||", self.logl[imageid]
			return l
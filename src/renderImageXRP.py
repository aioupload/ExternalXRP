#tejask@mit.edu - MIT Probabilistic Computing Group
from numpy import *
from math import *
import pdb

class renderImageXRP:
	def __init__(self,renderer):
		self.id_of_this_xrp = 10
		self.is_scorable = 0
		self.is_random_choice = 0
		self.name = "renderImageXRP"
		self.renderer = renderer

	def execXRP(self,args):
		things = []
		for i in range(0,len(args),6):
			if args[i+5] == '1':
				things.append({'left':int(args[i]), 'top':int(args[i+1]), 'id':chr(int(args[i+2])+65), 'size':int(args[i+3]), 'blur_sigsq':floor(float(args[i+4]))})
		
		self.renderer.get_rendered_image(things)
		#this is a big hack
		self.id_of_this_xrp = self.id_of_this_xrp + 1

	def getLogLikelihood(self,xrpid,pflip):
		return 0
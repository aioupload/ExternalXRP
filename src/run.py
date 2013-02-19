#tejask@mit.edu - MIT Probabilistic Computing Group

import os, sys
from loadImageXRP import *
from renderImageXRP import *
from noisyImageCompareXRP import *
from Renderer import *

lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from XRPServer import *

############ GLOBAL PARAMETERS ############
LOAD_IMAGE_XRP = 1
RENDER_XRP = 10
NOISYCOMP_XRP = 3



class runner(XRPServer):

	def __init__(self):
		super(runner, self).__init__()
		self.r = Renderer()


	def getXRPObject(self,XRPid):
		xrpOBJ = None
		if XRPid == LOAD_IMAGE_XRP:
			xrpOBJ = loadImageXRP(self.r)
		elif XRPid == RENDER_XRP:
			xrpOBJ = renderImageXRP(self.r)
		elif XRPid == NOISYCOMP_XRP:
			xrpOBJ = noisyImageCompareXRP(self.r)
		else:
			return None
		return xrpOBJ


	def execXRPFunc(self,XRPid,args):
		if XRPid >= RENDER_XRP: #this is a hack!
			XRPid = RENDER_XRP
		self.MMU[XRPid].execXRP(args)
		return self.MMU[XRPid].id_of_this_xrp #in our case xrpOBJid is same as XRPid


	def getLogLikelihood(self,XRPid,args):
		if XRPid >=RENDER_XRP: #this is a hack!
			XRPid = RENDER_XRP
		logscore = str(self.MMU[XRPid].getLogLikelihood(int(args[0]),float(args[1])))
		return logscore


## Start Server
server = runner()
while True:
	message = server.socket.recv() #Waiting for request
	ret = str(server.dispatch(message))



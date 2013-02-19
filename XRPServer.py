import zmq
import sys
from Renderer import *
import pdb

from loadImageXRP import *
from renderImageXRP import *
from noisyImageCompareXRP import *

# These correspond to Venture code
LOAD_IMAGE_XRP = 1
RENDER_XRP = 10
NOISYCOMP_XRP = 3

#Global parameters
MMU = dict()


r = Renderer()


class XRPServer():
	def __init__(self):
		self.MMU = dict()
		self.context = zmq.Context()
		print "Starting Server ..."
		self.port = 4444
		self.socket = context.socket(zmq.REP)
		self.socket.bind("tcp://*:" + str(port))


	def createnewXRP(XRPid):
		xrpOBJ = None
		if XRPid == LOAD_IMAGE_XRP:
			xrpOBJ = loadImageXRP(r)
		elif XRPid == RENDER_XRP:
			xrpOBJ = renderImageXRP(r)
		elif XRPid == NOISYCOMP_XRP:
			xrpOBJ = noisyImageCompareXRP(r)
		else:
			print "[ERROR] In createnewXRP - XRPid unindentified\n"
			return None
		MMU[XRPid] = xrpOBJ
		return xrpOBJ


def dispatch(message):
	#print message
	message = message.split(":")
	cmd = message[0]
	XRPid = int(message[1])

	if cmd == "LoadRemoteXRP":
		xrpOBJ = createnewXRP(XRPid)
		
		socket.send(str(xrpOBJ.id_of_this_xrp))

		message = socket.recv()
		socket.send(str(xrpOBJ.is_scorable))

		message = socket.recv()
		socket.send(str(xrpOBJ.is_random_choice))

		message = socket.recv()
		socket.send(str(xrpOBJ.name))
		return 

	elif cmd == "TemplateForExtendedXRP":
		if XRPid >= 10: #this is a hack!
			XRPid = 10
		MMU[XRPid].execFunc(message[2:])
		socket.send(str(MMU[XRPid].id_of_this_xrp)) #in our case xrpOBJid is same as XRPid

	elif cmd == "GetLogL":
		if XRPid >=RENDER_XRP: #this is a hack!
			XRPid = RENDER_XRP
		logscore = str(MMU[XRPid].getLogLikelihood(int(message[2]),float(message[3])))
		#print MMU[XRPid].name, "| getlog:", logscore
		socket.send(logscore)

	else:
		print "[ERROR] In dispatch - cannot recognize OPCODE"
		return -1


while True:
	#print "Waiting for clients ..."
	message = socket.recv()
	#print "Recieved reply", "[", message, "]"
	#print "###########"
	ret = str(dispatch(message))
	#print "###########"
	#print "Sending request"	, "...", ret


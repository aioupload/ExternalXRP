#tejask@mit.edu - MIT Probabilistic Computing Group

import zmq
import sys
import pdb


class XRPServer(object):

	def __init__(self):
		self.MMU = dict()
		self.context = zmq.Context()
		print "Starting Server ..."
		self.port = 4444
		self.socket = self.context.socket(zmq.REP)
		self.socket.bind("tcp://*:" + str(self.port))

	#Child class should implement this - contains dictionary of custom Objects per XRPid
	def getXRPObject(self,XRPid):
		raise NotImplementedError()

	def execXRPFunc(self,XRPid,args): #Child class should implement this - contains dictionary of custom Objects per XRPid
		raise NotImplementedError()

	def getLogLikelihood(self,XRPid,args):
		raise NotImplementedError()

	def createnewXRP(self,XRPid):
		self.MMU[XRPid] = self.getXRPObject(XRPid)
		if self.MMU[XRPid] is None:
			print "[ERROR] In createnewXRP - XRPid unindentified\n"
		return self.MMU[XRPid]

	#Message format: <CMD>:<XRPid>:<args[1...N]>
	def dispatch(self,message):
		#print message
		message = message.split(":")
		cmd = message[0]
		XRPid = int(message[1])

		if cmd == "LoadRemoteXRP":
			xrpOBJ = self.createnewXRP(XRPid)
			
			self.socket.send(str(xrpOBJ.id_of_this_xrp))

			message = self.socket.recv()
			self.socket.send(str(xrpOBJ.is_scorable))

			message = self.socket.recv()
			self.socket.send(str(xrpOBJ.is_random_choice))

			message = self.socket.recv()
			self.socket.send(str(xrpOBJ.name))
			return 

		elif cmd == "TemplateForExtendedXRP":
			id_of_XRP = self.execXRPFunc(XRPid,message[2:])
			self.socket.send(str(id_of_XRP))

		elif cmd == "GetLogL":
			logscore = self.getLogLikelihood(XRPid, message[2:])
			self.socket.send(logscore)

		else:
			print "[ERROR] In dispatch - cannot recognize OPCODE"
			return -1



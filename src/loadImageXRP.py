
class loadImageXRP:
	def __init__(self,renderer):
		self.id_of_this_xrp = 1
		self.is_scorable = 0
		self.is_random_choice = 0
		self.name = "loadImageXRP"
		self.renderer = renderer

	def execFunc(self,args):
		self.renderer.loadImage("")

	def getLogLikelihood(self,xrpid,pflip):
		return 0
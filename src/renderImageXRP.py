
class renderImageXRP:
	def __init__(self,renderer):
		self.id_of_this_xrp = 10
		self.is_scorable = 0
		self.is_random_choice = 0
		self.name = "renderImageXRP"
		self.renderer = renderer

	def execFunc(self,args):
		things = []
		things.append({'left':int(args[0]), 'top':int(args[1]), 'id':chr(int(args[2])+65), 'size':int(args[3]), 'blur_sigsq':int(float(args[4]))})
		self.renderer.get_rendered_image(things)
		#this is a big hack
		self.id_of_this_xrp = self.id_of_this_xrp + 1

	def getLogLikelihood(self,xrpid,pflip):
		return 0
class NODE(object):
	def __init__(self, x,y,movementCost):
		self.parent = None
		self.x = x
		self.y = y
		self.movementCost = movementCost
		self.g = 0
		self.h = 0
		self.f = 0
		
	def printState(self):
		print("x = %d y = %d movementCost = %d g = %d h = %d f = %d" % (self.x,self.y,self.movementCost,self.g,self.h,self.f))
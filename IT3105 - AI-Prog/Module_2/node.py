class NODE(object):
	
	def __init__(self, index, x_coord, y_coord, domain):
		self.index = index
		self.x_coord = x_coord
		self.y_coord = y_coord
		self.domain = [x for x in range(1,domain+1)]
		#self.domain = set([x for x in range(1,domain+1)])
		self.neighbours = set()
		
	def addNeighbour(self, n):
		self.neighbours.add(n)
		
	def printState(self):
		print("----------------")
		print("Index %d x_coord %d y_coord %d" % (self.index, self.x_coord, self.y_coord))
		list = []
		for node in self.neighbours:
			list.append(node.index)
		print("Neighbours: ", list)
		print("Domain: ", self.domain)
		print("-----------------")
	

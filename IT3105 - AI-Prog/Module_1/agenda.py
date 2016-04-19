import queue



class AGENDAQUEUE(object):
	def __init__(self, searchMethod):
		self.queue = set() #queue used for ASTAR
		self.queue_list = [] #queue used for dfs and bfs
		self.search_method = searchMethod
		
		
	def add(self, node):
		#SEARCHMETHOD defines which queue and at which index the node is added
		#ASTAR simply adds it to the set
		#DFS adds it to the front
		#BFS appends it to the end
		if self.search_method == "ASTAR":
			self.queue.add(node)
		elif self.search_method == "DFS" and node not in self.queue_list:
			self.queue_list.insert(0,node)
		elif self.search_method == "BFS" and node not in self.queue_list:
			self.queue_list.append(node)
		
	def pop(self):
		node = None
		#IF SEARCHMETHOD is ASTAR remove the one with smallest f value
		#ELSE just pop the first element of the queue
		if self.search_method == "ASTAR":
			#Get the node with the smallest f value from queue
			node = min(self.queue, key=lambda o:o.f)
			self.queue.remove(node)
		elif self.search_method == "DFS" or self.search_method == "BFS":
			node = self.queue_list.pop(0)
		return node
	
	def getLength(self):
		if self.search_method == "ASTAR":
			return len(self.queue)
		elif self.search_method == "DFS" or self.search_method == "BFS":
			return len(self.queue_list)
		
	def contains(self, node):
		if self.search_method == "ASTAR":
			return node in self.queue
		else:
			return node in self.queue_list
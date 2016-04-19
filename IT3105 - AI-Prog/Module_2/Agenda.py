import queue



class Agenda(object):
	def __init__(self, searchMethod):
		self.queue = [] #queue used for ASTAR
		self.queue_list = [] #queue used for dfs and bfs
		self.search_method = searchMethod
		
		
		
		
	def Add(self, state):
		#SEARCHMETHOD defines which queue and at which index the node is added
		#ASTAR simply adds it to the set
		#DFS adds it to the front
		#BFS appends it to the end
		if self.search_method == "ASTAR":
			if not self.Contains(state):
				self.queue.append(state)
		elif self.search_method == "DFS" and node not in self.queue_list:
			self.queue_list.insert(0,node)
		elif self.search_method == "BFS" and node not in self.queue_list:
			self.queue_list.append(node)
		
	def Pop(self):
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
	
	def GetLength(self):
		if self.search_method == "ASTAR":
			return len(self.queue)
		elif self.search_method == "DFS" or self.search_method == "BFS":
			return len(self.queue_list)
		
	def Contains(self, state):
		domain_list = []
		match = False
		for node in state.nodes:
			domain_list.append(node.domain)
			
		for instance in self.queue:
		
			intermediate_match = True
			for i in range(0,len(domain_list)):
				if instance.nodes[i] != domain_list[i]:
					intermediate_match = False
					break
			if intermediate_match:
				match = True
				break
					
		return match
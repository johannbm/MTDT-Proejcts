class GAC_VERTEXCOLORING_SPECIALIZATION(object):


	def revise(self, focal, other_variables,constraint, csp):
		revised = False
		otherValue = other_variables[0]
		#Loop through each value of the focals domain
		for x in csp.domain[focal.index]:
			match = False
			#Look for a variable in the other_variable domain that satisfies the constraint
			for y in csp.domain[otherValue.index]:
				if constraint(x,y):
					match = True
					break
			if match == False:
				csp.domain[focal.index].remove(x)
				revised = True
		return revised
		
	def initialization(self, csp, constraint):
		queue = []
		for node in csp.nodes:
			for neighbour in node.neighbours:
				queue.append([node,neighbour, constraint])
					
		return queue
	
	def rerun(self, state, constraint):
		queue = []
		for n in state.assumptionNode.neighbours:
			queue.append([n, state.assumptionNode, constraint])
			
		return queue
		
	def addNewRevisedArcs(self, Xi, Xj, constraint):
		queue = []
		neighbours = Xi.neighbours.copy()
		for n in neighbours:
			if n != Xj:
				queue.append([n, Xi, constraint])
		return queue
	
	def isSolution(self, state, constraint):
		for key in state.domain:
			if len(state.domain[key]) != 1:
				return False
			for n in state.getNodeByIndex(key):
				if not constraint(state.domain[key], state.domain[n.index]):
					return False
		return True
		#for key in state.domain:
		#	if len(state.domain[key]) != 1:
		#		return False
			
		
		for node in state.nodes:
			if len(state.domain) != 1:
				return False
			for n in node.neighbours:
				if len(n.domain) != 1:
					return False
				if not (self.constraint(min(node.domain), min(n.domain))):
					return False
					
		return True
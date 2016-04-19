from csp import *
import random
import copy

class ASTAR_VC_SPECIALIZATION(object):
	
	def getHeuristic(self, csp):
		total = len(csp.nodes)
		for key in csp.domain:
			if len(csp.domain[key]) == 1:
				total -= 1
		return total

		
	def getNeighbours(self, csp):
		neighbours = []
		var = csp.getNodeWithSmallestDomain()
		#for value in self.randomiseDomainList(csp.domain[var]):
		for value in csp.domain[var]:
			new = csp.copyCSP()
			new.domain[var] = [value]
			new.assumptionNode = new.getNodeByIndex(var)
			neighbours.append(new)
		return neighbours
		
	def isSolution(self, state, constraint):
		for key in state.domain:
			if len(state.domain[key]) != 1:
				return False
			for n in state.getNodeByIndex(key).neighbours:
				if not constraint(state.domain[key], state.domain[n.index]):
					return False
		return True
		
	def getPathLength(self, state):
		total = 1
		while state.parent != None:
			total += 1
			state = state.parent
			
		return total
	
		
	def randomiseDomainList(self, l):
		randomList = []
		
		while len(l) > 0:
			randomIndex = random.randrange(0,len(l))
			value = l[randomIndex]
			l.remove(value)
			randomList.append(value)
		return randomList
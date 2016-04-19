from Agenda import *
from csp import *
from node import *
from aStarVertexColoringSpecialization import *
import copy

class ASTAR(object):
	
	def __init__(self, gac):
		self.nodesCreated = 0
		self.gacReference = gac
		self.specialization = ASTAR_VC_SPECIALIZATION()
		
		
	def pathfinder(self, cspState):
		current = None
		solutionState = None
		open = Agenda("ASTAR")
		closed = set()
		open.Add(cspState)
		cspState.h = self.specialization.getHeuristic(cspState)
		cspState.f = cspState.g + cspState.h
		while open.GetLength() > 0:
			self.nodesCreated += 1
			current = open.Pop()
			closed.add(current)
			print("Assumed node: ", "Not assigned" if current.assumptionNode is None else current.assumptionNode.index)
			print("Current f value: ", current.f)
			
			for nextNode in self.specialization.getNeighbours(current):
								
				if nextNode in closed:
					continue

				res = self.gacReference.gacRerun(nextNode)
				if (not res):
					closed.add(nextNode)
					continue
				nextNode.f = self.specialization.getHeuristic(nextNode)
				if (self.specialization.isSolution(nextNode, self.gacReference.constraint)):
					solutionState = nextNode
					break
				if not open.Contains(nextNode):
					nextNode.parent = current
					open.Add(nextNode)
			if self.specialization.isSolution(nextNode, self.gacReference.constraint):
				break
		
		if isinstance(solutionState, CSP):
			print("FOUND SOLUTION")
			solutionState.printState()
			print("NODES VISITED: ", self.nodesCreated)
			print("SEARCH TREE SIZE: ", len(closed) + open.GetLength())
			print("LENGTH OF SOLUTION PATH: ", self.specialization.getPathLength(solutionState))
			return solutionState
		return False
import copy
import math
from Agenda import *
from nonogramSpecialization import *

class ASTAR(object):

	def __init__(self, reference):
		self.nodesCreated = 0
		self.gacReference = reference
		self.specialization = NONOGRAM_SPECIALIZATION()

	def getCurrentPath(self, node):
		#Returns the path to the startNode from node.
		nodes = []
		while node.parent != None:
			nodes.append(node)
			node = node.parent
		nodes.append(node)
		return nodes
		
	def updateNodeCosts(self, next_node, node):
		#Update next_nodes costs and parent
		next_node.g = node.g + node.movementCost
		next_node.h = self.specialization.getHeuristic(next_node)
		next_node.parent = node
		next_node.f = next_node.g + next_node.h
			
	def pathfinder(self, state):
		current = None
		solution_state = None
		#Create an open list. SEARCHMETHOD (ASTAR/BFS/DFS) defines what type of queue open will act like
		open = Agenda("ASTAR")
		#Create closed set. Ensure uniqueness
		closed = set()
		#Add the startNode to open and calculate its values
		open.Add(state)
		state.h = self.specialization.getHeuristic(state)
		state.f = state.g + state.h
		while open.GetLength() > 0:
			self.nodesCreated += 1
			print("popping node: ", self.nodesCreated)
			current = open.Pop()
			closed.add(current)
			for next_node in self.specialization.getNearbyNodes(current):
				
				if next_node in closed:
					continue

				#Call GAC-Rerun, break if it has found a solution
				res = self.gacReference.rerun(next_node)
				next_node.f = self.specialization.getHeuristic(next_node)
				if (not res):
					closed.add(next_node)
					continue
				if (next_node.isSolution()):
					solution_state = next_node
					break
				#Update the costs and if node not in open add it.
				if open.Contains(next_node):
					if next_node.g > current.g + current.movementCost:
						self.updateNodeCosts(next_node, current)
				else:
					self.updateNodeCosts(next_node, current)
					open.Add(next_node)
			if (next_node.isSolution()):
				break
		
		if solution_state != None:
			print("Nodes expanded: ", self.nodesCreated)
			print("Solution depth: ", len(self.getCurrentPath(solution_state)))
			#self.gacReference.gui.drawCSP(solution_state)
			return True
			
		return False
				





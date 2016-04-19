import os
import datetime
from csp import *
from node import *
from gacVertexColoringSpecialization import *
from Agenda import *
from astar import *
from gui import *
import random
sys.setrecursionlimit(10000)
import copy

class GAC(object):

	#This is the general arc consistency class which will be "subclassed" by the class
	#pointed to by specialization, all problem specific formulations will be implemented there
	
	def __init__(self,k, cspProblem, scale_value, x_offset, y_offset, heuristic, animate):
		self.constraint = self.makeConstraint(["a","b"],'a!=b')
		self.csp = CSP(cspProblem, k)
		self.specialization = GAC_VERTEXCOLORING_SPECIALIZATION()
		self.gui = GUI(self.csp.nodes, scale_value, x_offset, y_offset, animate)
		self.astar = ASTAR(self)
		
		solutionState = None
		
		#Start measuring time to solve
		startTime = datetime.datetime.now()
		
		#Solve by using different heuristics
		if heuristic == 0:
			solutionState = self.backtrack(self.csp)[1]
		elif heuristic == 1:
			solutionState = self.gacExecution()
		#elif heuristic == 2:
			
		endTime = datetime.datetime.now()

		
		if isinstance(solutionState, CSP):
			self.gui.colorGraph(solutionState)
			print("UNSATISFIED CONSTRAINTS: ", solutionState.getNumberOfUnsatisfiedConstraints(self.constraint))
			print("VERTICES WITHOUT COLOR ASSIGNMENT: ", solutionState.getNumberOfVerticesWithouColor())
		else:
			print('Failure')
		
		print("Time spent: ", int((endTime - startTime).total_seconds() * 1000), " ms")
			
		self.gui.getMouse()
		
				
	def getNodeByIndex(self, index):
		for x in self.nodes:
			if x.index == index:
				return x
		return None
			
	def makeConstraint(self, var_names, expression, envir=globals()):
		args = ""
		for n in var_names:
			args = args + "," + n
		return eval("(lambda " + args[1:] + ": " + expression + ")", envir)
		
	def gacExecution(self):
	
		#Initialize the queue to be used for the first domain filtering, prior to doing A* guesses
		queue = self.specialization.initialization(self.csp, self.constraint)
		
		#DOMAIN-FILTERING
		result = self.domainFilteringLoop(queue, self.csp)
		
		if result and not self.specialization.isSolution(self.csp, self.constraint):
			return self.astar.pathfinder(self.csp)
		elif not result:
			return False
		
		return True
	
	#Returns a randomized list, that may be used when generating neighbours
	def randomiseDomainList(self, l):
		randomList = []
		
		while len(l) > 0:
			randomIndex = random.randrange(0,len(l))
			value = l[randomIndex]
			l.remove(value)
			randomList.append(value)
		return randomList
			
			
	def domainFilteringLoop(self, queue, csp):
		while queue:
			e = queue.pop(0)
			Xi = e[0]
			Xj = e[1]
			c = e[2]
			if self.specialization.revise(Xi,[Xj],c, csp):
				if len(csp.domain[Xi.index]) == 0:
					return False
				elif len(csp.domain[Xi.index]) > 1:
					self.gui.removeColor(Xi)
				queue.extend(self.specialization.addNewRevisedArcs(Xi,Xj,c))
			
			if len(csp.domain[Xi.index]) == 1:
				self.gui.colorNode(Xi.index,csp.domain[Xi.index])

		return True
		
	def gacRerun(self, state):
		queue = self.specialization.rerun(state, self.constraint)
		return self.domainFilteringLoop(queue, state)
		
	def astarSearch(self, state):
		#Start Astar search, with state_0 as root
		return Pathfinder(state, self)
		
	def backtrackRevise(self, csp):
		queue = []
		for node in csp.nodes:
			for neighbour in node.neighbours:
				queue.append([node,neighbour,self.constraint])
		return self.domainFilteringLoop(queue)
		
	def backtrack(self, csp):
		if self.specialization.isSolution(csp, self.constraint):
			return [True, csp]
		var = csp.getNodeWithSmallestDomain()
		for value in self.randomiseDomainList(var.domain):
			new = copy.deepcopy(csp)
			new.getNodeByIndex(var.index).domain = [value]
			revisedResult = self.backtrackRevise(new)
			
			if revisedResult:
				result = self.backtrack(new)
				if result[0]:
					return result
					
		return [False, csp]
			
	
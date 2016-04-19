from node import *
import copy

class CSP(object):

	def __init__(self, cspProblem, numberOfColors):
		self.h = 0
		self.g = 0
		self.f = 0
		self.parent = None
		self.assumptionNode = None
		info = cspProblem[0].split(' ')
		self.numberOfVertices = eval(info[0])
		self.numberOfEdges = eval(info[1])	
		self.nodes = self.createNodes(cspProblem[1:self.numberOfVertices+1], numberOfColors)
		self.createEdges(cspProblem[self.numberOfVertices+1:])
		self.domain = self.initializeDomain(numberOfColors, len(self.nodes))
		
	def createNodes(self, cspProblem, numberOfColors):
		nodes = []
		for i in range(len(cspProblem)):
			nodeInfo = cspProblem[i].split(' ')
			nodes.append(NODE(eval(nodeInfo[0]), eval(nodeInfo[1]), eval(nodeInfo[2]), numberOfColors))
			
		return nodes
		
	def initializeDomain(self, numOfColors, length):
		dom = {}
		for i in range(length):
			dom[i] = [x for x in range(1, numOfColors+1)]
		
		return dom
		
		
	def copyCSP(self):
		domain = copy.deepcopy(self.domain)
		newCSP = copy.copy(self)
		self.domain = domain
		return newCSP
	
	def getNumberOfUnsatisfiedConstraints(self, constraint):
		total = 0
		for node in self.nodes:
			for n in node.neighbours:
				if not constraint(self.domain[node.index], self.domain[n.index]):
					total += 1
					
		return total
		
	def getNumberOfVerticesWithouColor(self):
		total = 0
		for key in self.domain:
			if len(self.domain[key]) != 1:
				total += 1
				
		return total
			
	
	def printState(self):
		print(self.domain)
		print("------")
	
	def createEdges(self, cspProblem):
		for i in range(len(cspProblem)):
			nodeInfo = cspProblem[i].split(' ')
			node1 = eval(nodeInfo[0])
			node2 = eval(nodeInfo[1])
			self.getNodeByIndex(node1).addNeighbour(self.getNodeByIndex(node2))
			self.getNodeByIndex(node2).addNeighbour(self.getNodeByIndex(node1))
				
	def getNodeByIndex(self, index):
		for x in self.nodes:
			if x.index == index:
				return x
				
		return None
		
		
	def getMaxNode(self):
		max = 0
		index = -1
		for key in self.domain:
			if len(self.domain[key]) > max:
				max = len(self.domain[key])
				index = key
		return index
		
	def getNodeWithSmallestDomain(self):
		#node = max(self.domain.items(), key=lambda o:len(o))[0]
		node = self.getMaxNode()
		
		for n in self.nodes:
			if len(self.domain[n.index]) > 1:
				if len(self.domain[n.index]) <= len(self.domain[node]):
					node = n.index
		return node

		
		
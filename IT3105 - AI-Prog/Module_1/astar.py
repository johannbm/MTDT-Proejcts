from graphics import *
from node import *
from agenda import *
from gui import *
import math

class ASTAR(object):
	
	def __init__(self, dim, start, goal, barriers, searchMethod):
		self.navigationGrid = [[]]
		self.open = AGENDAQUEUE(searchMethod)
		self.closed = set()
		self.nodes = []
		self.startNode = None
		self.goalNode = None
		self.nodesCreated = 0
		self.createNavigationMap(dim, start, goal, barriers)
		self.gui = GUI(self.nodes, 20, self.startNode, self.goalNode)
		self.gui.drawGrid()

	def createNavigationMap(self, dim, start, goal, barriers):
		#Creates a navigation grid (nested lists) representing the board and adds given barriers
		self.navigationGrid = [[0 for y in range(dim[1])] for x in range(dim[0])]
		self.navigationGrid = self.addBarriers(self.navigationGrid, barriers)
		
		#Creates node objects representing each tile on the board
		#Wall nodes are given a movement cost of 10000 rather than just being impassable (allows extension for terrain navigation)
		for x in range(dim[0]):
			for y in range(dim[1]):
				self.nodes.append(NODE(x,y,1.0 if self.navigationGrid[y][x] == 0 else 10000))
		self.startNode = self.getNode(start[0], dim[1] - 1 - start[1])
		self.goalNode = self.getNode(goal[0], dim[1] - 1 - goal[1])
		self.startNode.h = self.getHeuristic(self.startNode)
		self.startNode.f = self.startNode.g + self.startNode.h
	
	def addBarriers(self, grid, bar):
		for b in bar:
			for i in range(b[2]):
				for j in range(b[3]):
					grid[b[1]+j][b[0]+i] = 1
			
		grid = list(reversed(grid))	
		return grid
		
	def getNode(self, y,x):
		#Returns the node from the list of nodes with the given x and y coordinates
		return self.nodes[y * len(self.navigationGrid) + x]

	def getNearbyNodes(self, node):
		#Returns all neighboring nodes of node in 4 directions; north, west, south, east.
		nearbyNodes = []
		x = node.x
		y = node.y
		if (y - 1 >= 0):
			nearbyNodes.append(self.getNode(x,y-1))
		if (x + 1 <= len(self.navigationGrid[y])-1):
			nearbyNodes.append(self.getNode(x+1,y))
		if (x - 1 >= 0):
			nearbyNodes.append(self.getNode(x-1,y))
		if (y + 1 <= len(self.navigationGrid)-1):
			nearbyNodes.append(self.getNode(x,y+1))
			
		return nearbyNodes
	
	def getCurrentPath(self, node):
		#Returns the path to the startNode from node.
		nodes = []
		while node.parent != None:
			nodes.append(node)
			node = node.parent
		nodes.append(node)
		return nodes
	
	def getHeuristic(self, node):
		#Manhattan distance to the target
		#return math.fabs(node.x - self.goalNode.x) + math.fabs(node.y - self.goalNode.y)
		#Euclidean distance to target
		return math.sqrt(math.fabs(node.x - self.goalNode.x)**2 + math.fabs(node.y - self.goalNode.y)**2)
	
	def updateNodeCosts(self, nextNode, node):
		#Update next_nodes costs and parent
		nextNode.g = node.g + node.movementCost
		nextNode.h = self.getHeuristic(nextNode)
		nextNode.parent = node
		nextNode.f = nextNode.g + nextNode.h
		
	def pathfinder(self, animateGraphics = "y"):
		#Add the startNode to open and calculate its values
		self.open.add(self.startNode)
		while self.open.getLength() > 0:
			self.nodesCreated += 1
			current = self.open.pop()
			if current is self.goalNode:
				self.debugPath()
				self.gui.drawPath(self.getCurrentPath(self.goalNode), self.open, self.closed)
				break
				
			self.closed.add(current)
			
			#For each successing node, ignore walls (cost > 1) and nodes already in the closed list
			for nextNode in self.getNearbyNodes(current):
				if nextNode.movementCost > 1.0:
					continue
				if nextNode in self.closed:
					continue
					
				#Update the costs and if node not in open add it.
				if self.open.contains(nextNode):
					if nextNode.g > current.g + current.movementCost:
						self.updateNodeCosts(nextNode, current)
				else:
					self.updateNodeCosts(nextNode, current)
					self.open.add(nextNode)
				
			if animateGraphics == "y":
				self.gui.drawPath(self.getCurrentPath(current), self.open, self.closed)
		print("open length: ", self.open.getLength())
		print("closed length: ", len(self.closed))
				
	def debugPath(self):
		path = self.getCurrentPath(self.goalNode)
		for node in path:
			node.printState()
		print ("found solution")
		print ("Path length: ", len(path))
		print ("Nodes created: ", self.nodesCreated)

def PrintGrid(grid):
	for x in grid:
		print (x)

#def DrawMaze(window, nodeList, nodeSize):
#	global GraphicsMapping
#	
#	for node in nodeList:
#		rect = Rectangle(Point(node.x*nodeSize,node.y*nodeSize),Point((node.x+1)*nodeSize,(node.y+1)*nodeSize))
#		if node.movementCost > 1:
#			rect.setFill('red')
#		else:
#			rect.setFill('white') 
#		rect.draw(window)
#		GraphicsMapping[(node.x, node.y)] = rect
#			
#def DrawMazeUpdate(window, nodeList, currentNode):
#	global GraphicsMapping
#	
#	curPath = GetCurrentPath(currentNode)
#	for node in nodeList:
#		rect = GraphicsMapping[(node.x, node.y)]
#		if node.movementCost > 1:
#			rect.setFill('red')
#		elif node not in curPath:
#			rect.setFill('white')
#		if node is GoalNode or node is StartNode:
#			rect.setFill('yellow')
#	for node in curPath:
#		rect = GraphicsMapping[(node.x, node.y)]
#		rect.setFill('green')








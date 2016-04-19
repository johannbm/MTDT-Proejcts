from graphics import *

class GUI(object):
	
	def __init__(self, nodes, nodeSize,startNode, goalNode):
		self.window = GraphWin(width = 800, height = 800)
		self.nodes = nodes
		self.rects = {}
		self.startNode = startNode
		self.goalNode = goalNode
		self.nodeSize = nodeSize
		
	def drawGrid(self):
		for node in self.nodes:
			rect = Rectangle(Point(node.x*self.nodeSize,node.y*self.nodeSize),Point((node.x+1)*self.nodeSize,(node.y+1)*self.nodeSize))
			rect.setFill('white')
			if node.movementCost > 1:
				rect.setFill('red')
			rect.draw(self.window)
			self.rects[(node.x, node.y)] = rect
		self.colorEndNodes()
	
	
	def drawPath(self, pathNodes, openList, closedList):
		for node in self.nodes:
			if node.movementCost > 1 or node is self.startNode or node is self.goalNode:
				continue
			rect = self.rects[(node.x, node.y)]
			rect.setFill('white')
			if node in closedList:
				rect.setFill('orange')
			elif openList.contains(node):
				rect.setFill('brown')
			if node in pathNodes:
				rect.setFill('pink')
		self.colorEndNodes()
				
	def colorEndNodes(self):
		self.rects[(self.startNode.x, self.startNode.y)].setFill('yellow')
		self.rects[(self.goalNode.x, self.goalNode.y)].setFill('green')
			
	
	
	def getMouse(self):
		self.window.getMouse()
			
			
	
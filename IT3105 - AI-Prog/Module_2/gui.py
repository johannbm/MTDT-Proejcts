from graphics import *
from random import randint

class GUI(object):
	
	def __init__(self, nodes, scale_value, x_offset, y_offset, animate):
		self.win = GraphWin('Vertex Coloring', 1400, 1000)
		self.scale_value = scale_value
		self.x_offset = x_offset
		self.y_offset = y_offset
		self.animate = animate
		self.node_dict = []
		self.drawNodes(nodes)
	
	def drawNodes(self, nodes, override = False):
		if not self.animate and not override:
			return
		for node in nodes:		
			for neighbour in node.neighbours:
				line = Line(self.resizePoint(Point(node.x_coord, node.y_coord)), self.resizePoint(Point(neighbour.x_coord, neighbour.y_coord)))
				line.setFill(self.getRandomColor())
				line.draw(self.win)
			cir = Circle(self.resizePoint(Point(node.x_coord, node.y_coord)), 7)
			self.node_dict.insert(node.index, cir)
			
		for cir in self.node_dict:
			cir.draw(self.win)
			
	def getMouse(self):
		self.win.getMouse()
	
	def resizePoint(self, point):
		p_x = (point.x + self.x_offset) * self.scale_value
		p_y = (point.y + self.y_offset) * self.scale_value
		return Point(p_x, p_y)
		
	def colorGraph(self, state):
		if not self.animate:
			self.drawNodes([n for n in state.nodes], True)
		for node in state.nodes:
			self.colorNode(node.index, state.domain[node.index], True)
	
	def colorNode(self, index, domain, override = False):
		if not self.animate and not override:
			return
		node_graphic = self.node_dict[index]
		node_graphic.setFill(self.getColor(domain))
		
	def removeColor(self, node):
		if not self.animate:
			return
		node_graphic = self.node_dict[node.index]
		node_graphic.setFill('white')
			
	def getColor(self, domain):
		if domain == [1]:
			return 'red'
		if domain == [2]:
			return 'green'
		elif domain == [3]:
			return 'blue'
		elif domain == [4]:
			return 'yellow'
		elif domain == [5]:
			return 'black'
		elif domain == [6]:
			return color_rgb(100,100,100)
			
	def getRandomColor(self):
		return color_rgb(randint(0,255),randint(0,255),randint(0,255))
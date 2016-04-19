from graphics import *

class GUI(object):
	
	def __init__(self, rowCount, columnCount):
		self.win = GraphWin('Nonograms', 1400, 1000)
		self.rectangles = [[0 for x in range(rowCount)] for y in range(columnCount)]
		self.tileWidth = 20
		self.tileHeight = 20
		self.drawBoard()
		
	def drawBoard(self):
		for x in range(len(self.rectangles)):
			for y in range(len(self.rectangles[x])):
				self.rectangles[x][y] = Rectangle(Point(self.tileWidth*x, y*self.tileHeight), Point((x+1)*self.tileWidth,(y+1)*self.tileHeight))
				self.rectangles[x][y].draw(self.win)
	
	def drawCSP(self, csp):
		for x in csp.rowVariables:
			if len(csp.rowVariables[x]) == 1:
				self.colorRowOrColumn(x, csp.rowVariables[x][0], True)
		for y in csp.columnVariables:
			if len(csp.columnVariables[y]) == 1:
				self.colorRowOrColumn(y, csp.columnVariables[y][0], False)

	def colorRowOrColumn(self, n, values, isRow):
		if isRow:
			for x in range(len(values)):
				self.colorTile(x,n, values[x])
		else:
			for y in range(len(values)):
				self.colorTile(n,y, values[y])
				
	def colorTile(self, x, y, color):
		if color == 0:
			self.rectangles[x][y].setFill('white')
		elif color == 1:
			self.rectangles[x][y].setFill('grey')
			
	def getMouse(self):
		self.win.getMouse()
				
				
#gui = GUI(10,10)
#gui.drawBoard()
#gui.colorRowOrColumn(2, [1,1,1,1,1,1,1,1,1,1], True)
#gui.colorTile(2,2,1)
#gui.win.getMouse()

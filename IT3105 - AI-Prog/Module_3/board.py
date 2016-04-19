import copy
import math
from csp import *
from gui import *
from astar import *
from nonogramGacSpecialization import *

class BOARD(object):
	
	def __init__(self, rowCount, columnCount, rowConstraints, columnConstraints):
		#REMINDER: reverse column when entering values
		#self.rows = [[0 for x in range(rowCount)] for y in range(columnCount)]
		#self.columns = [[0 for x in range(rowCount)] for y in range(columnCount)]
		self.specialization = NONOGRAM_GAC_SPECIALIZATION()
		self.rowCount = rowCount
		self.columnCount = columnCount
		
		self.rowConstraints = rowConstraints
		self.columnConstraints = columnConstraints
		self.gui = GUI(rowCount, columnCount)
		self.astar = ASTAR(self)
		self.csp = CSP(rowConstraints, columnConstraints)
		self.csp.generateVariableDomain(rowConstraints, columnConstraints)
		res = self.gacExecution()
		if res:
			self.gui.drawCSP(self.csp)
		print("result ", res)
		self.gui.getMouse()
		
		
	def gacExecution(self):
		#INITIALIZATION
		self.drawInitial()
		queue = self.specialization.initialize(self.csp)

				
		#DOMAIN-FILTERING
		result = self.domainFilteringLoop(queue)
		if result and not self.csp.isSolution():
			return self.astar.pathfinder(self.csp)
		elif not result:
			return False
		
		
		return True
		
	def drawInitial(self):
		for x in range(self.rowCount):
			if len(self.csp.rowVariables[x]) == 1:
				self.gui.colorRowOrColumn(x,self.csp.rowVariables[x][0], True)
		for y in range(self.columnCount):
			if len(self.csp.columnVariables[y]) == 1:
				self.gui.colorRowOrColumn(y,self.csp.columnVariables[y][0], False)
		
	def domainFilteringLoop(self, queue):
		while queue:
			e = queue.pop(0)
			rowNumber = e[0]
			colNumber = e[1]
			source = e[2]
			if self.specialization.revise(rowNumber, colNumber, source, self.csp):
				if len(self.csp.getVariable(rowNumber, source)) == 0:
					return False
				#draw
				elif len(self.csp.getVariable(rowNumber, source)) == 1:
					self.gui.colorRowOrColumn(rowNumber,self.csp.getVariable(rowNumber, source)[0], source)
				queue.extend(self.specialization.newRevisedArcs(self.csp, source, rowNumber, colNumber))
						
		print("state after domain filtering")
		self.csp.printState()
		return True

	def rerun(self, state):
		self.csp = state
		queue = self.specialization.rerunGetArcs(state)
		return self.domainFilteringLoop(queue)
	
		
		

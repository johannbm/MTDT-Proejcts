class NONOGRAM_GAC_SPECIALIZATION(object):

		
	def initialize(self, csp):
		queue = []
		for i in range(len(csp.rowVariables)):
			for j in range(len(csp.columnVariables)):
				queue.append([i, j, True])
				queue.append([j,i,False])
		return queue
		
	def newRevisedArcs(self, csp, source, rowNumber, colNumber):
		queue = []
		if source:
			for key in csp.columnVariables:
				if key != colNumber:
					queue.append([key, rowNumber, not source])
		else:
			for key in csp.rowVariables:
				if key != colNumber:
					queue.append([key, rowNumber, not source])
					
		return queue
		
	def revise(self,rowNumber, colNumber, isRow, csp):
		if isRow:
			row = csp.rowVariables[rowNumber]
			column = csp.columnVariables[colNumber]
		else:
			row = csp.columnVariables[rowNumber]
			column = csp.rowVariables[colNumber]
		#Does all the domains in the column variable of the shared cell agree on the same value
		isAllBlanks = True
		isAllFilled = True
		for col in column:
			if col[rowNumber] == 1:
				isAllBlanks = False
			elif col[rowNumber] == 0:
				isAllFilled = False				
		#If Every space is filled, remove all rows that is not filled
		
		revised = False
		if isAllFilled:
			for r in list(row):
				if r[colNumber] == 0:
					#print("deleted ",r)
					print(csp.getNumberOfRowCombinations())
					revised = True
					row.remove(r)
					
		if isAllBlanks:
			for r in list(row):
				if r[colNumber] == 1:
					#print("deleted ",r)
					revised = True
					row.remove(r)
		return revised
		
	def rerunGetArcs(self, state):
		queue = []
		isRow = state.assumptionIndex[1]
		if isRow:
			for key in state.rowVariables:
				queue.append([key, state.assumptionIndex[0], False])
		else:
			for key in state.columnVariables:
				queue.append([key, state.assumptionIndex[0], True])
				
		return queue
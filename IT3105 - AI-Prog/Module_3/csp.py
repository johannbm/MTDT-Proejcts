import copy

class CSP(object):
	
	def __init__(self, rowConstraints, columnConstraints):
		self.rowVariables = {}
		self.columnVariables = {}
		self.rowConstraints = rowConstraints
		self.columnConstraints = columnConstraints
		self.parent = None
		self.g = 0
		self.h = 0
		self.f = 0
		self.movementCost = 0
		self.assumptionIndex = []
	
	
	def printState(self):
		for key in self.rowVariables:
			print ("---ROW:",key,"---", "   ","constraint: ",self.rowConstraints[key])
			for value in self.rowVariables[key]:
				print(value)
				
		for key in self.columnVariables:
			print ("---COLUMN:",key,"---", "   ","constraint: ",self.columnConstraints[key])
			for value in self.columnVariables[key]:
				print(value)

				
	def getVariable(self, n, isRow):
		if isRow:
			return self.rowVariables[n]
		else:
			return self.columnVariables[n]
	
	def getHeuristic(self):
		total = 0
		#Loop through all rows, add the the size of domain to total
		for x in self.rowVariables:
			total += len(self.rowVariables[x]) - 1
		for y in self.columnVariables:
			total += len(self.columnVariables[y]) - 1
		return total
		
	def isSolution(self):
		for x in self.rowVariables:
			if len(self.rowVariables[x]) != 1:
				return False
				
		for y in self.columnVariables:
			if len(self.columnVariables[y]) != 1:
				return False
				
		return True
	
	def generateVariableDomain(self, rowConstraints, columnConstraints):
		#Enumerate all rows
		print("asdasd", rowConstraints)
		for x in range(len(rowConstraints)):		
			self.rowVariables[x] = self.generateCombinationsForConstraint(rowConstraints[x],len(columnConstraints))
		for y in range(len(columnConstraints)):
			self.columnVariables[y] = self.generateCombinationsForConstraint(columnConstraints[y],len(rowConstraints))
			
		#quick debug for counting all possibilities
		totalRow = 0
		for key in self.rowVariables:
			totalRow += len(self.rowVariables[key])
			
		print("totalRow ", totalRow)
			
			
	def getNumberOfRowCombinations(self):
		totalRow = 0
		for key in self.rowVariables:
			totalRow += len(self.rowVariables[key])
		return totalRow
			
	def generateCombinationsForConstraint(self, constraint, length):
		if len(constraint) == 1 and constraint[0] == 0:
			return [[0]*length]
		originalInitial = self.initializeFirstEnumeration(constraint)
		rows = []
		freeSpaces = length - self.getSumOfConstraint(constraint) - (len(constraint) - 1)
		possiblePlaces = len(constraint) + 1
		#numberOfCombinations = math.factorial(freeSpaces + possiblePlaces-1)/(math.factorial(possiblePlaces-1)*math.factorial((freeSpaces + possiblePlaces-1)-(possiblePlaces-1)))
		spaceList = list(self.enumerate(possiblePlaces,freeSpaces))
		for t in spaceList:
			initial = copy.copy(originalInitial)
			for i in range(len(t)):
				if t[i] > 0:
					for j in range(t[i]):
						initial.insert(self.getIndexOfNthConstraint(initial,i),0)
			rows.append(initial)
			
		for row in rows:
			self.replaceNumbersWithOnes(row)
		
		return rows
			
		
		
	def enumerate(self,n,s):
		if n == 1:
			yield (s,)
		else:
			for i in range(s + 1):
				for j in self.enumerate(n - 1,s - i):
					yield (i,) + j


		
		
	
	def initializeFirstEnumeration(self,constraint):
		l = []
		
		for c in constraint:
			l.append(c)
			l.append(0)
		del l[-1]
		return l
		
	def replaceNumbersWithOnes(self, l):
		i = 0
		while i < len(l):
			if l[i] > 1:
				l[i:i+1] = [1]*l[i]
				i += l[i]
			i += 1
		
	
				
	def getIndexOfNthConstraint(self, l,n):
		
		counter = 0
		for i in range(len(l)):
			if l[i] != 0:
				if counter == n:
					return i
				else:
					counter += 1
		return len(l)
		
		
	def getSumOfConstraint(self, constraint):
		tot = 0
		for x in constraint:
			tot += x
		return tot
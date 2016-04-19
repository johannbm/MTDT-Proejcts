from csp import *

class NONOGRAM_SPECIALIZATION(object):
	
	def getHeuristic(self, state):
		#Manhattan distance to the target
		return state.getHeuristic()
		
	def getNearbyNodes(self, state):
		states = []
		
		#Enumerate all possible states
		for x in state.rowVariables:
			if len(state.rowVariables[x]) > 1:
				for i in range(len(state.rowVariables[x])):
					newState = copy.deepcopy(state)
					newState.assumptionIndex = [x, True]
					newState.rowVariables[x] = [state.rowVariables[x][i]]
					states.append(newState)
		for y in state.columnVariables:
			if len(state.columnVariables[y]) > 1:
				for i in range(len(state.columnVariables[y])):
					newState = copy.deepcopy(state)
					newState.assumptionIndex = [y, False]
					newState.rowVariables[y] = [state.columnVariables[y][i]]
					states.append(newState)

		return states
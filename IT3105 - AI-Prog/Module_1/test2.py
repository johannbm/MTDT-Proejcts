from graphics import *
from Node import *
from Agenda import *
import math

NavigationGrid = [[]]
Nodes = []
StartNode = None
GoalNode = None
GraphicsMapping = {}
NodesCreated = 0

def CreateNavigationMap(dim, start, goal, barriers):
	global NavigationGrid
	global StartNode
	global GoalNode
	NavigationGrid = [[0 for y in range(dim[1])] for x in range(dim[0])]
	NavigationGrid = AddBarriers(NavigationGrid, barriers)
	
	for x in range(dim[0]):
		for y in range(dim[1]):
			Nodes.append(Node(x,y,1 if NavigationGrid[y][x] == 0 else 10000))
	StartNode = GetNode(start[0], dim[1] - 1 - start[1])
	GoalNode = GetNode(goal[0], dim[1] - 1 - goal[1])
	
def AddBarriers(grid, bar):
	for b in bar:
		for i in range(b[2]):
			for j in range(b[3]):
				grid[b[1]+j][b[0]+i] = 1
		
	grid = list(reversed(grid))	
	return grid
		
def GetNode(y,x):
	return Nodes[y * len(NavigationGrid) + x]

def GetNearbyNodes(node):
	nearbyNodes = []
	x = node.x
	y = node.y
	if (x - 1 >= 0):
		nearbyNodes.append(GetNode(x-1,y))
	if (x + 1 <= len(NavigationGrid[y])-1):
		nearbyNodes.append(GetNode(x+1,y))
	if (y - 1 >= 0):
		nearbyNodes.append(GetNode(x,y-1))
	if (y + 1 <= len(NavigationGrid)-1):
		nearbyNodes.append(GetNode(x,y+1))
		
	return nearbyNodes
	
def PrintGrid(grid):
	for x in grid:
		print (x)

	
def PrintNodeInfo(node):
	print("x = %d y = %d movementCost = %d g = %d h = %d f = %d" % (node.x,node.y,node.movementCost,node.g,node.h,node.f))

def GetCurrentPath(node):
	nodes = []
	while node.parent != None:
		nodes.append(node)
		node = node.parent
	nodes.append(node)
	return nodes
	
def DrawMaze(window, nodeList, nodeSize):
	global GraphicsMapping
	
	for node in nodeList:
		rect = Rectangle(Point(node.x*nodeSize,node.y*nodeSize),Point((node.x+1)*nodeSize,(node.y+1)*nodeSize))
		if node.movementCost > 1:
			rect.setFill('red')
		else:
			rect.setFill('white') 
		rect.draw(window)
		GraphicsMapping[(node.x, node.y)] = rect
			
def DrawMazeUpdate(window, nodeList, currentNode):
	global GraphicsMapping
	
	curPath = GetCurrentPath(currentNode)
	for node in nodeList:
		rect = GraphicsMapping[(node.x, node.y)]
		if node.movementCost > 1:
			rect.setFill('red')
		elif node not in curPath:
			rect.setFill('white')
		if node is GoalNode or node is StartNode:
			rect.setFill('yellow')
	for node in curPath:
		rect = GraphicsMapping[(node.x, node.y)]
		rect.setFill('green')
	
def GetHeuristic(node):
	return math.fabs(node.x - GoalNode.x) + math.fabs(node.y - GoalNode.y)
	
def UpdateNodeCosts(next_node, node):
	next_node.g = node.g + node.movementCost
	next_node.h = GetHeuristic(next_node)
	next_node.parent = node
	next_node.f = next_node.g + next_node.h
		
def Pathfinder():
	global NodesCreated
	open = set()
	closed = set()
	open.add(StartNode)
	StartNode.h = GetHeuristic(StartNode)
	StartNode.f = StartNode.g
	while open:
		NodesCreated += 1
		current = min(open, key=lambda o:o.f)
		if current is GoalNode:
			DebugPath()
			DrawMazeUpdate(win, Nodes, current)
			break
		open.remove(current)
		closed.add(current)
		for next_node in GetNearbyNodes(current):
			if next_node.movementCost > 1:
				continue
			if next_node in closed:
				continue
			if next_node in open:
				if next_node.g > current.g + current.movementCost:
					UpdateNodeCosts(next_node, current)
			else:
				UpdateNodeCosts(next_node, current)
				open.add(next_node)
			
		
		DrawMazeUpdate(win, Nodes, current)
	win.getMouse()
			
def DebugPath():
	global GoalNode
	print ("found solution")
	path = GetCurrentPath(GoalNode)
	print ("Path length: ", len(path))
	print ("Nodes created: ", NodesCreated)


index = eval(input("Enter index (blank line if custom): "))
if index != "":
	if index == 0:
		barriers = [[2,3,5,5],[8,8,2,1]]
		dim = [10,10]
		goalNode = [9,9]
		startNode = [0,0]
	elif index == 1:
		barriers = [[5,5,10,10],[1,2,4,1]]
		dim = [20,20]
		goalNode = [2,18]
		startNode = [19,3]
	elif index == 2:
		barriers = [[17,10,2,1],[14,4,5,2],[3,16,10,2],[13,7,5,3],[15,15,3,3]]
		dim = [20,20]
		goalNode = [19,19]
		startNode = [0,0]
	elif index == 3:
		barriers = [[3,0,2,7],[6,0,4,4],[6,6,2,4]]
		dim = [10,10]
		goalNode = [9,5]
		startNode = [0,0]
	elif index == 4:
		barriers = [[3,0,2,7],[6,0,4,4],[6,6,2,4]]
		dim = [10,10]
		goalNode = [9,9]
		startNode = [0,0]
	elif index == 5:
		barriers = [[4,0,4,16],[12,4,2,16],[16,8,4,4]]
		dim = [20,20]
		goalNode = [19,13]
		startNode = [0,0]
	
else:
	barriers = []
	inp = "."
	while inp != "":
		inp = input("Keep entering barriers, exit with blank line: ")
		if inp != "":
			barrier = eval(inp)
			barriers.append(barrier)

	dim = eval(input("Enter dimensions: ")) #Gets the dimensions. Should be formatted as a list.
	startNode = eval(input("Enter start: "))
	goalNode = eval(input("Enter goal: "))

win = GraphWin(width = 800, height = 800)
#CreateNavigationMap([6,6],[1,0],[5,5],[[3,2,2,2],[0,3,1,3],[2,0,4,2],[2,5,2,1]])
CreateNavigationMap(dim, startNode, goalNode, barriers)
DrawMaze(win, Nodes, 20)
Pathfinder()
nodes = GetNearbyNodes(GetNode(0,1))

PrintGrid(NavigationGrid)




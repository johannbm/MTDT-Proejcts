from graphics import *
from Node import *
from Agenda import *
import math

NavigationGrid = [[]]
Nodes = []
StartNode = None
GoalNode = None
GraphicsMapping = {}

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
		else:
			rect.setFill('white')
		if node is GoalNode or node is StartNode:
			rect.setFill('yellow')
	for node in curPath:
		rect = GraphicsMapping[(node.x, node.y)]
		rect.setFill('green')
	
def GetHeuristic(node):
	return math.fabs(node.x - GoalNode.x) + math.fabs(node.y - GoalNode.y)
	
def UpdateNodeCosts(n, node):
	n.g = node.g + n.movementCost
	n.h = GetHeuristic(n)
	n.parent = node
	n.f = n.g + n.h
		
def Pathfinder():
	global Nodes
	global Window
	closedList = set()
	openList = Agenda()
	openList.Push(StartNode)
	while openList.GetSize():
		node = openList.Pop()[2]
		closedList.add(node)
		if node is GoalNode:
			DebugPath()
			DrawMazeUpdate(win, Nodes, node)
			break
		successors = GetNearbyNodes(node)
		for n in successors:
			if n in closedList:
				continue
			if openList.Contains(n):
				if node.g + node.movementCost < n.g: 
					n.g = node.g + node.movementCost
					n.f = n.g+n.h
					n.parent = node
			else:
				n.g = node.g + node.movementCost
				n.h = GetHeuristic(n)
				n.f = n.g+n.h
				n.parent = node
				openList.Push(n)
	
		DrawMazeUpdate(win, Nodes, node)
	win.getMouse()
			
def DebugPath():
	global GoalNode
	print ("found solution")
	n = GoalNode
	while n.parent != None:
		PrintNodeInfo(n)
		n = n.parent
	
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




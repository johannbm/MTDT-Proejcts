from astar import *

#Start of the program
#Sets up data needed for doing navigation tests		
index = input("Enter index (blank line if custom): ")
if index == "":
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
else:
	index = eval(index)
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
	

searchMethod = input("Enter Search method (ASTAR/BFS/DFS): ")
animateGraphics = input("Animate graphics: (y/n): ")

astar = ASTAR(dim, startNode, goalNode, barriers, searchMethod)
astar.pathfinder()
astar.gui.getMouse()

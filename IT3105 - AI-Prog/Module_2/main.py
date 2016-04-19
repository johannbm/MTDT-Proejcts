import os
from gac import *

def getProblemInfo():
	scale_value = 5
	x_offset = 20
	y_offset = 20
	index = input("Enter problem index(blank for custom): ")
	if index == "":
		k = eval(input("Enter number of colors: "))
		file_path = input("Enter file path: ")
	else:
		index = eval(index)
		file_path = ""
		k=4
		if index == 0:
			file_path = "graph-color-1.txt"
			scale_value = 10
		elif index == 1:
			file_path = "graph_color_2.txt"
		elif index == 2:
			file_path = "rand-50-4-color1.txt"
		elif index == 3:
			file_path = "rand-100-4-color1.txt"
		elif index == 4:
			file_path = "rand-100-6-color1.txt"
			k=5
		elif index == 5:
			file_path = "spiral-500-4-color1.txt"
			k=4
			scale_value = 0.025
			x_offset = 15000
			y_offset = 12000
			
	heuristic = eval(input("Enter heuristic to be used: BACKTRACKING(0), MRV(1), MN(2): "))
	animate = eval(input("Animate graphics(True/False): "))
			
	dir = os.path.dirname(__file__)
	file_path = os.path.join(dir, file_path)
	f = open(file_path,'r')
	GAC(k,f.readlines(), scale_value, x_offset, y_offset, heuristic, animate)
	return None
	
getProblemInfo()
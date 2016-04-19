import os
from board import *

def evalList(l):
	for i in range(len(l)):
		l[i] = l[i].split(' ')
		for j in range(len(l[i])):
			l[i][j] = eval(l[i][j])

index = eval(input("Enter problem index scenario: "))
if index == 0:
	file_path = "nono-heart-1.txt"
elif index == 1:
	file_path = "nono-cat.txt"
elif index == 2:
	file_path = "nono-chick.txt"
elif index == 3:
	file_path = "nono-rabbit.txt"
elif index == 4:
	file_path = "nono-camel.txt"
elif index == 5:
	file_path = "nono-telephone.txt"
elif index == 6:
	file_path = "nono-sailboat.txt"
elif index == 7:
	file_path = "lol.txt"
elif index == 8:
	file_path = "washington.txt"
elif index == 9:
	file_path = "b.txt"
elif index == 10:
	file_path = "puzzle3.txt"
elif index == 11:
	file_path = "key.txt"
elif index == 12:
	file_path = "cola.txt"
elif index == 13:
	file_path = "nono-example.txt"
elif index == 14:
	file_path = "nono-clover.txt"

dir = os.path.dirname(__file__)
file_path = os.path.join(dir, file_path)
f = open(file_path,'r')

fileContent = f.readlines()

dimensions = fileContent[0].split(' ')
dimensions[0] = eval(dimensions[0])
dimensions[1] = eval(dimensions[1])
rowConstraints = fileContent[1:dimensions[1]+1]
columnConstraints = fileContent[dimensions[1]+1:]
evalList(rowConstraints)
evalList(columnConstraints)
#Reverse rowConstraints
rowConstraints = rowConstraints[::-1]

print(dimensions[0])
print(rowConstraints)
print(dimensions[1])
print(columnConstraints)

board = BOARD(dimensions[1], dimensions[0], rowConstraints, columnConstraints)
#board.generateAllPossibleRowCombinations2()

from visuals import GameWindow
from logic import *
import math
import theano.tensor as T
import scipy
from random import randint
from ai2048demo import *
import time
from main import *
from tkinter import *
from preprocessor import *
import copy


def move(dir, board):
	#input is a 1d board state, convert to matrix
	board = decompress(board)
	matrix = [board[0:4],board[4:8],board[8:12],board[12:]]
	res = None
	executed = None
	if dir == 0:
		res, executed = up(matrix)
	elif dir == 1:
		res, executed = right(matrix)
	elif dir == 2:
		res, executed = down(matrix)
	else:
		res, executed = left(matrix)

	board = [item for sublist in res for item in sublist]
	return compress(board), executed


def decompress(board):
	for i in range(len(board)):
		if board[i] > 0:
			board[i] = 2**board[i]
	return board
	
def compress(board):
	for i in range(len(board)):
		if board[i] > 0:
			board[i] = int(math.log(board[i],2))
	return board
	
def spawn_tile(board):
	empty_index = []
	for i in range(len(board)):
		if board[i] == 0:
			empty_index.append(i)
	if len(empty_index) == 0:
		return False
	slot = empty_index[randint(0, len(empty_index)-1)]
	chance = randint(0,9)
	board[slot] = 1 if chance < 9 else 2
	return True
	
	
def print_board(board):
	print("-----------------")
	matrix = [board[0:4],board[4:8],board[8:12],board[12:]]
	for i in matrix:
		print(i, "\n")
	print("-----------------")

def get_ranked_moves(moves):
	return sorted(range(len(moves)), key=lambda k: moves[k])
	
def is_game_over(board):
	state = copy.copy(board)
	game_over = True
	for i in range(4):
		state = copy.copy(board)
		executed = move(i, copy.copy(board))[1]
		if executed:
			game_over = False
			break
	return game_over
		

def get_score(results):
	tot = 0
	for i in results:
		tot += sum(i)
	print("num of res: ", len(results))
	return tot / (len(results*16))
		
def simulate_runs(k=50):
	results = []
	for i in range(k):
		board = [0]*16
		spawn_tile(board)
		while True:
			dir = randint(0,3)
			board, executed = move(dir,board)
			if executed:
				spawned = spawn_tile(board)
				if is_game_over(board):
					break
		results.append(2**max(board))
	
	
	#print("Score: ", get_score(results))
	return results

def visualize_AI_run(a):
	root = Tk()
	window = GameWindow(root)
	board = [0]*16
	spawn_tile(board)
	def run_AI(board, root):

		b = preprocess([board])
		res = a.propagate_forward(b[0], get_all = True)
		res = get_ranked_moves(res)
		executed = None
		for m in res:
			board, executed = move(m, board)
			if executed:
				window.update_view(board)
				break
		spawn_tile(board)
		if is_game_over(board):
			return
		window.update_view(board)
		root.after(3000, run_AI(board, root))
	root.after(1, run_AI(board, root))
	root.mainloop()
	
def simulate_AI_runs(a, k=50):
	results = []
	moves = []
	
	for i in range(k):
		board = [0]*16
		spawn_tile(board)
		while True:
			b = preprocess([board])
			res = a.propagate_forward(b[0], get_all = True)
			res = get_ranked_moves(res)
			for m in res:
				board, executed = move(m, board)
				if executed:
					moves.append(m)
					break
			spawn_tile(board)
			if is_game_over(board):
				break
		results.append(2**max(board))
		
	#print("Score AI: ", get_score(results))
	return results
	

def test_config(topology = [19,4], lr = 0.001, repeat = 1, dataset = "human - normalized"):
	
	total = []
	r = []
	for i in range(repeat):
		a = Ann(topology, 4)
		train(a)
		resai = simulate_AI_runs(a)

		resrand = simulate_runs()
		f = open('res', 'a')
		w = welch(resrand, resai)
		print(w)
		print("average random: ", sum(resrand) / len(resrand))
		print("average ai: ", sum(resai) / len(resai))
		r.append(scipy.stats.ttest_ind(resrand, resai, equal_var=False)[1])
		res = "Topology: " + str(topology) + " lr: " + str(lr) + " dataset: " + dataset + "\n"
		res += w
		f.write(res)
		try:
			total.append(eval(w[-4:-3]))
		except:
			f.write(str(0))
			total.append(0)
		f.close()
		#print(welch(resrand, resai))
	print(total)
	print("avg: ", sum(total) / len(total))
	print("avg P-val: ", sum(r) / len(r))
	f = open('res', 'a')
	s = "avg: " +  str(sum(total) / len(total)) + "\n"
	f.write(s)
	f.close()

test_config()

input()
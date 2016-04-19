import math
import copy

def monotonicity(board):
	res = []
	for state in board:
		mono = []
		
		mono.append(get_vertical_mono_score(state, lambda a: a > 0))
		mono.append(get_vertical_mono_score(state, lambda a: a < 0))
		mono.append(get_horizontal_mono_score(state, lambda a: a > 0))
		mono.append(get_horizontal_mono_score(state, lambda a: a < 0))
		
		normalize(mono)
		
		res.append(mono)
	return res
	
def corner_tile(board):
	res = []
	for state in board:
		l = [state[0], state[3], state[15], state[12]]
		m = max(l)
		ll = [0,0,0,0]
		for i in range(4):
			if l[i] == m:
				ll[i] = 1
				break
		res.append(ll)
				
	return res
			
		
	
def get_vertical_mono_score(board, cond):
	score = 0
	for j in range(4):
		for i in range(3):
			diff = board[(i+1)*4+j] - board[i*4+j]
			if cond(diff):
				score += int(math.fabs(diff))
				
	return score
	
	
def get_horizontal_mono_score(board, cond):
	score = 0
	for j in range(4):
		for i in range(3):
			diff = board[(i+1)+(j*4)] - board[i+(j*4)]
			if cond(diff):
				score += int(math.fabs(diff))
				
	return score
	

def my_way(state):
	temp = []
	#temp.append(top_row(state))
	s = smoothness(state)
	temp.append(s[0])
	temp.append(s[1])
	temp.append(max([state[0],state[3], state[12], state[15]]))
	#temp.append(top_mono(state))
	temp.append(get_vertical_mono_score(state, lambda a: a > 0))
	temp.append(get_vertical_mono_score(state, lambda a: a < 0))
	temp.append(get_horizontal_mono_score(state, lambda a: a > 0))
	temp.append(get_horizontal_mono_score(state, lambda a: a < 0))
	#scale(temp)
	#print(temp)
	return temp

def preprocess(board):
	res = []
	for state in board:
		res.append(snake_way(state))
	return res
	
def snake_way(state):
	res = []
	snake = [10,8,7,6.5,.5,.7,1,3, -.5,-1.5,-1.8,-2, -3.8,-3.7,-3.5,-3]
	for i in range(16):
		res.append(state[i]*snake[i])
	
	#scale(res)
	return res

	
def top_row(state):
	return sum([2 for x in state[0:4] if x > 0])
	
def top_mono(state):
	score = 0
	for i in range(3):
		diff = state[i+1] - state[i]
		if diff > 0:
			score -= diff
	return score
	
def smoothness(state):
	hor_state = [x for x in copy.copy(state) if x > 0]
	hor_score = 0
	for i in range(len(hor_state)-1):
		hor_score += hor_state[i] if hor_state[i] == hor_state[i+1] else 0
	vert_score = 0
	vert_state = transpose(state)
	for i in range(len(vert_state)-1):
		vert_score += vert_state[i] if vert_state[i] == vert_state[i+1] else 0
	
	return hor_score, vert_score
	
def transpose(state):
	l = []
	for i in range(4):
		for j in range(4):
			l.append(state[i+j*4])
	return l
	
	
def normalize(l):
	tot = sum(l)
	if tot > 0:
		l[:] = [x / tot for x in l]
		
def scale(l):
	m = max(l)
	if m > 0:
		l[:] = [x / m for x in l]
	
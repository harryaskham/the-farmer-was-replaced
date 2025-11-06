from lib import *

def inc_bounded(state, key, n=1):
	state[key] = (state[key] + n) % wh(state)
	return state
	
def inc_x(state, n=1):
	return inc_bounded(state, "x", n)
	
def inc_y(state, n=1):
	return inc_bounded(state, "y", n)

def moveM(state, d, update_tail=False):
	prev = xy_tup(state)
	
	if not move(d):
		return state

	if d == North:
		state = inc_y(state)
	elif d == South:
		state = inc_y(state, -1)
	elif d == East:
		state = inc_x(state)
	elif d == West:
		state = inc_x(state, -1)
		
	if update_tail:
		state["tail"].append(prev)
		if len(state["tail"]) > state["tail_len"]:
			if state["tail"][0] in state["tail_set"]:
				state["tail_set"].remove(state["tail"][0])
			state["tail"] = state["tail"][1:]
		state["tail_set"].add(prev)
		
	return state
	
def move_boundedM(state, dir, update_tail=False):
	[x, y] = xy(state)
	d = wh(state)
	if x == d-1 and dir == East:
		return state
	if x == 0 and dir == West:
		return state
	if y == d-1 and dir == North:
		return state
	if y == 0 and dir == South:
		return state
	return moveM(state, dir, update_tail)
		
def go_originM(state):
	return move_to(state, [0, 0])

def move_to(state, c):
	[cx, cy] = c
	while x(state) > cx:
		state = moveM(state, West)
	while x(state) < cx:
		state = moveM(state, East)
	while y(state) > cy:
		state = moveM(state, South)
	while y(state) < cy:
		state = moveM(state, North)
	return state
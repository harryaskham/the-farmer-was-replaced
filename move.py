from lib import *

def inc_bounded(state, key, n=1):
	state, d = wh(state)
	state[key] = (state[key] + n) % d
	return state
	
def inc_x(state, n=1):
	return inc_bounded(state, "x", n)
	
def inc_y(state, n=1):
	return inc_bounded(state, "y", n)

def moveM(state, d, update_tail=False):
	state, prev = xy_tup(state)
	
	if not move(d):
		return state
		
	state = maybe_update_excursion(state, d)

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
	
def move_bounded(state, dir, update_tail=False):
	state, [x, y] = xy(state)
	state, d = wh(state)
	if x == d-1 and dir == East:
		return state
	if x == 0 and dir == West:
		return state
	if y == d-1 and dir == North:
		return state
	if y == 0 and dir == South:
		return state
	return moveM(state, dir, update_tail)
		
def move_to(state, c):
	cx, cy = unpack(c)
	while x(state)[1] > cx:
		state = moveM(state, West)
	while x(state)[1] < cx:
		state = moveM(state, East)
	while y(state)[1] > cy:
		state = moveM(state, South)
	while y(state)[1] < cy:
		state = moveM(state, North)
	return state

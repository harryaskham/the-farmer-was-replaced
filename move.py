from lib import *

def moveM(state, d):
	if not move(d):
		return state	
	if d == North:
		state["y"] += 1
	elif d == South:
		state["y"] -= 1
	if d == East:
		state["x"] += 1
	elif d == West:
		state["x"] -= 1
	return state
	
def move_boundedM(state, d):
	[x, y] = xy(state)
	n = wh(state)
	if x == n-1 and d == East:
		return state
	if x == 0 and d == West:
		return state
	if y == n-1 and d == North:
		return state
	if y == 0 and d == South:
		return state
	if not move(d):
		return state	
	if d == North:
		state["y"] += 1
	elif d == South:
		state["y"] -= 1
	if d == East:
		state["x"] += 1
	elif d == West:
		state["x"] -= 1
	return state
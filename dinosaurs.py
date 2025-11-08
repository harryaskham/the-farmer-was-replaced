from lib import *
from sense import *
from move import *
from pathing import *

def set_apple(state):
	state, e = et(state)
	state, c = xy(state)
	if e != E.Apple or c != state["apple"]:
		return state
	return set_state(state, {
		"apple": measure()
	})
	
def brute(state):
	xd = East
	yd = North
	state, d = wh(state)
	[w, h] = [d, d]
	while True:
		state, [x, y] = xy(state)
		if x == 0:
			xd = East
		if x == w - 1:
			xd = West
		if y == 0:
			yd = North
			state = moveM(state, xd)
		if y == h - 1:
			yd = South
			state = moveM(state, xd)
		state = moveM(state, yd)
		if xy(state)[1] == [x, y]:
			return state

def dumb(state):
	while True:
		state = sense(state)
	
		if state["apple"] == None:
			return state
	
		(ax, ay) = state["apple"]
		state, [x, y] = xy(state)
		
		ds = []
		if x > ax:
			ds.append(West)
		if x < ax: 
			ds.append(East)
		if y < ay:
			ds.append(North)
		if y > ay:
			ds.append(South)
		for d in [North, East, South, West]:
			ds.append(d)
		moved = False
		for d in ds:
			state, moved = move_bounded(state, d)
			if moved:
				break
		if not moved:
			return state

def apple_here(state):
	return set_state(state, { "apple": xy(state) })
	
def search_apple(state):
	while True:
		state = sense(state)
		state["tail_len"] += 1
		state = debug(state, ["apple", state["apple"], "len", state["tail_len"], "pos", xy_tup(state)[1]], 2, "search")
		#state, path = path_to(state, state["apple"])
		state, path = path_to(state, state["apple"], False)
		if path == None:
			return state

		for dir in path:
			state = moveM(state, dir, [Dinosaur.UPDATE_TAIL])

def dino(state, policies, delay=0):
	for policy in policies:
		state = do_(state, [
			[hatM, Hats.Straw_Hat],
			[hatM, Hats.Dinosaur_Hat],
			[set_state, { "tail": [] }],
			[set_state, { "tail_set": set() }],
			[set_state, { "tail_len": 0 }],
			[policy],
			[wait_secsM, delay],
			[hatM, Hats.Straw_Hat],
			[set_state, { "apple": None }],
			[set_state, { "tail": [] }],
			[set_state, { "tail_set": set() }],
			[set_state, { "tail_len": 0 }],
		])
	return state

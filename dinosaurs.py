from lib import *
from sense import *
from move import *

def hatM(state, hat):
	change_hat(hat)
	return state

def set_apple(state):
	if et(state) != E.Apple or xy(state) != state["apple"]:
		return state
	return set_state(state, {
		"apple": measure()
	})
	
def brute(state):
	xd = East
	yd = North
	[w, h] = [wh(state), wh(state)]
	while True:
		[x, y] = xy(state)
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
		if xy(state) == [x, y]:
			return state

def dumb(state):
	while True:
		state = sense(state, False)
	
		if state["apple"] == None:
			return state
	
		(ax, ay) = state["apple"]
		[x, y] = xy(state)
			
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
			state = move_boundedM(state, d)
			if xy(state) != [x, y]:
				moved = True
				break
		if not moved:
			return state

def apple_here(state):
	return set_state(state, { "apple": xy(state) })

def dino(state, policy):
	while True:
		state = dos(state, [
			[hatM, Hats.Wizard_Hat],
			[hatM, Hats.Dinosaur_Hat],
			[policy],
			[hatM, Hats.Wizard_Hat],
			[set_state, { "apple": None }]
		])
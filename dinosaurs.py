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

def dumb(state):
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
	for d in ds:
		state = moveM(state, d)
		if xy(state) != [x, y]:
			return dumb(state)
	return state

def apple_here(state):
	return set_state(state, { "apple": xy(state) })

def dino(state, policy):
	return dos(state, [
		[hatM, Hats.Wizard_Hat],
		[hatM, Hats.Dinosaur_Hat],
		[policy],
		[hatM, Hats.Wizard_Hat],
		[set_state, { "apple": None }]
	])
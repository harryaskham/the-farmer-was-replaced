from lib import *
from excursion import *
from sense import *

def moveM(state, d, flags=[]):
	flags = set(flags)
	state, prev = xy_tup(state)
	
	if not move(d):
		return state

	state = do_(state, [
		[sense, flags],
		[unless, Movement.REWIND_EXCURSION in flags, [maybe_update_excursion, d]]
	])

	state["here"] = state["grid"][state["y"]][state["x"]]
		
	if Dinosaur.UPDATE_TAIL in flags:
		state["tail"].append(prev)
		if len(state["tail"]) > state["tail_len"]:
			if state["tail"][0] in state["tail_set"]:
				state["tail_set"].remove(state["tail"][0])
			state["tail"] = state["tail"][1:]
		state["tail_set"].add(prev)
		
	return state
	
def move_bounded(state, dir, flags=[]):
	flags = set(flags)
	state, [x, y] = xy(state)
	state, d = wh(state)
	if x == d-1 and dir == East:
		return pure(state, False)
	if x == 0 and dir == West:
		return pure(state, False)
	if y == d-1 and dir == North:
		return pure(state, False)
	if y == 0 and dir == South:
		return pure(state, False)
	state = moveM(state, dir, flags)
	return pure(state, True)
		
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

def end_excursion(state):
	excursion = state["excursions"].pop()
	while excursion != []:
		d = excursion.pop()
		state = moveM(state, opposite(d), [Movement.REWIND_EXCURSION])
	return state

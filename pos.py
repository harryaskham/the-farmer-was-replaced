from monad import *
from aliases import *

def x(state):
	return pure(state, state["x"])
	
def y(state):
	return pure(state, state["y"])
	
def xy(state):
	state, sx = x(state)
	state, sy = y(state)
	return pure(state, [sx, sy])

def xy_tup(state):
	state, [x, y] = xy(state)
	return pure(state, (x, y))
	
def wh(state):
	return pure(state, state["wh"])

def et(state):
	return get_here(state, "entity_type")
	
def gt(state):
	return get_here(state, "ground_type")

def at(state, c):
	x, y = unpack(c)
	state, d = wh(state)
	if x < 0 or y < 0 or x >= d or y >= d:
		return unit(state)
	return pure(state, state["grid"][y][x])
		
def here(state):
	state, c = xy(state)
	return at(state, c)
	
def get_at(state, c, key=None):
	if key == None:
		return at(state, c)
	else:
		state, xs = at(state, c)
		return pure(state, xs[key])
	
def set_at(state, c, fields, flags=[]):
	flags = set(flags)
	x, y = unpack(c)
	states = [state]
	if To.CHILDREN in flags:
		for child_id in state["child_states"]:
			child_state = state["child_states"][child_id]
			states.append(child_state)

	for state in states:
		if Copy.CELL in flags:
			state["grid"][y][x] = merge(state["grid"][y][x], fields)
		else:
			for k in fields:
				state["grid"][y][x][k] = fields[k]
	
	return states[0]

def get_here(state, key=None):
	state, c = xy(state)
	return get_at(state, c, key)
	
def set_here(state, fields, flags=[]):
	state, c = xy(state)
	return set_at(state, c, fields, flags)
	
def opposite(d):
	return {
		North: South,
		South: North,
		East: West,
		West: East
	}[d]
	
def ixy(state, id=None):
	if id == None:
		id = state["id"]
	state, d = wh(state)
	y = 0
	while id >= d:
		id -= d
		y += 1
	x = id
	return pure(state, (x, y))

def start_excursion(state):
	state["excursions"].append([])
	return state
	
def current_excursion(state):
	if state["excursions"] == []:
		return unit(state)
	return pure(state, state["excursions"][-1])
	
def maybe_update_excursion(state, direction):
	state, excursion = current_excursion(state)
	if excursion == None:
		return state
	excursion.append(direction)
	return state
	
def end_excursion(state):
	excursion = state["excursions"].pop()
	while excursion != []:
		d = excursion.pop()
		state = moveM(state, opposite(d))
	return state
	
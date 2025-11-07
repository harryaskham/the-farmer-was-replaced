from monad import *
from aliases import *

def x(state=None):
	if state == None:
		return get_pos_x()
	return state["x"]
	
def y(state=None):
	if state == None:
		return get_pos_y()
	return state["y"]
	
def xy(state=None):
	return [x(state), y(state)]

def xy_tup(state=None):
	return (x(state), y(state))
	
def wh(state=None):
	if state == None:
		return get_world_size()
	return state["wh"]

def et(state=None):
	if state == None:
		return get_entity_type()
	return get_here(state, "entity_type")
	
def etM(state):
	v = et(state)
	return pure(state, v)
	
def gt(state=None):
	if state == None:
		return get_ground_type()
	return get_here(state, "ground_type")

def at(state, c):
	x, y = unpack(c)
	if x < 0 or y < 0 or x >= wh(state) or y >= wh(state):
		return None
	return state["grid"][y][x]
		
def here(state):
	return at(state, xy(state))
	
def get_at(state, c, key=None):
	if key == None:
		return at(state, c)
	else:
		return at(state, c)[key]
	
def set_at(state, c, fields, flags=[]):
	flags = set(flags)
	[x, y] = c
	states = [state]
	if To.CHILDREN in flags:
		for child_id in state["child_states"]:
			child_state = state["child_states"][child_id]
			states.append(child_state)

	for state in states:
		if Copy.CELL in flags:
			state["grid"][y][x][k] = merge(state["grid"][y][x], fields)
		else:
			for k in fields:
				state["grid"][y][x][k] = fields[k]
	
	return states[0]

def get_here(state, key=None):
	return get_at(state, xy(state), key)
	
def set_here(state, fields, flags=[]):
	return set_at(state, xy(state), fields, flags)
	
def go_origin():
	while x() > 0:
		move(West)
	while y() > 0:
		move(South)

def at_row_end():
	return x() == wh() - 1
	
def at_col_end():
	return y() == wh() - 1
	
def at_end():
	return at_row_end() and at_col_end()
	
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
	d = wh(state)
	y = 0
	while id >= d:
		id -= d
		y += 1
	x = id
	return (x, y)
	
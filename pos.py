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
	
def wh(state=None):
	if state == None:
		return get_world_size()
	return state["wh"]

def et(state=None):
	if state == None:
		return get_entity_type()
	return get_here(state, "entity_type")
	
def gt(state=None):
	if state == None:
		return get_ground_type()
	return get_here(state, "ground_type")

def at(state, c):
	[x, y] = c
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
	
def set_at(state, c, fields, copy=False):
	[x, y] = c
	if copy:
		state["grid"][y][x][k] = merge(state["grid"][y][x], fields)
	else:
		for k in fields:
			state["grid"][y][x][k] = fields[k]
	return state

def get_here(state, key=None):
	return get_at(state, xy(state), key)
	
def set_here(state, fields):
	return set_at(state, xy(state), fields)
	
def go_origin():
	while x() > 0:
		move(East)
	while y() > 0:
		move(South)

def at_row_end():
	return x() == wh() - 1
	
def at_col_end():
	return y() == wh() - 1
	
def at_end():
	return at_row_end() and at_col_end()
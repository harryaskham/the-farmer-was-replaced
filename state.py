from lib import *
from grid import *

def mk_state():
	g = mk_grid()
	here_x = x()
	here_y = y()
	return {
		"i": 0,
		"x": here_x,
		"y": here_y,
		"wh": wh(),
		"grid": g,
		"here": g[here_y][here_x],
		"ret": [],
		"error": None,
		"apple": None,
		"num_drones": 1,
		"max_drones": max_drones(),
		"child_handles": {},
		"child_states": {},
		"this_id": 0,
		"treasure": None
	}
	
def set_state(state, kvs, children=False):
	for k in kvs:
		state[k] = kvs[k]
	if children:
		for child_id in state["child_states"]:
			child_state = state["child_states"][child_id]
			for k in kvs:
				child_state[k] = kvs[k]
	return state
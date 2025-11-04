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
		"apple": None,
		"max_drones": max_drones(),
		"child_drones": {
		},
		"this_drone": 0,
		"treasure": None
	}
	
def set_state(state, kvs, children=True):
	for k in kvs:
		state[k] = kvs[k]
	for child in state["child_drones"]:
		child_state = state["child_drones"][child]
		for k in kvs:
			child_state[k] = kvs[k]
	return state
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
		"child_drones": []
	}
	
def set_state(state, kvs):
	for k in kvs:
		state[k] = kvs[k]
	return state
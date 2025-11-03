from lib import *

def spawnM(state, f):
	h = spawn_drone(f)
	if h != None:
		state["child_drones"].append(h)
	return state
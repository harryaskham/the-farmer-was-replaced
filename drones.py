from lib import *

def spawnM(state, f, delay=0):
	child_state = copy(state)
	
	def g():
		if delay > 0:
			wait_secs(delay)
		return dos(child_state, [f])
		
	child = spawn_drone(g)
	if child != None:
		child_state["this_drone"] = child
		state["child_drones"][child] = child_state
	return state
from lib import *
from debug import *

def next_child_id(state):
	return pure(state, num_drones())
	
def update_drone_state(state):
	state["num_drones"] = num_drones()
	return state
	
def can_spawn(state):
	state = update_drone_state()
	return state["num_drones"] < state["max_drones"]	
	
def must_spawn(state, f, delay=0):
	n = len(state["child_handles"])
	while len(state["child_handles"]) == n:
		state = spawnM(state, f, delay)
	return state

def spawnM(state, f, delay=0):
	state, child_id = dos(state, [[next_child_id]])
	child_state = merge(state, {
		"this_id": child_id
	})

	def g():
		if delay > 0:
			wait_secs(delay)
		return dos(child_state, [f])
		
	child = spawn_drone(g)
	if child != None:
		state["child_states"][child_id] = child_state
		state["child_handles"][child_id] = child
	return state
	
def wait_for_child(state, child_id):
	wait_for(state["child_handles"][child_id])
	return state
	
def wait_all(state):
	for child_id in state["child_handles"]:
		handle = state["child_handles"][child_id]
		wait_for(handle)
	state["child_handles"] = {}
	state["child_states"] = {}
	return state
from lib import *
from debug import *

def next_child_id(state):
	return pure(state, num_drones())
	
def update_drone_state(state):
	state["num_drones"] = num_drones()
	return state
	
def can_spawn(state):
	return dos(state, [
		[update_drone_state],
		[pure, state["num_drones"] < state["max_drones"]]
	])
	
def must_spawn(state, f, flags=[]):
	flags = set(flags)
	
	if Spawn.AWAIT in flags:
		flags.remove(Spawn.AWAIT)
		
	if Spawn.BECOME in flags:
		return spawnM(state, f, flags)
		
	n = len(state["child_handles"])
	while len(state["child_handles"]) == n:
		state = spawnM(state, f)
	return state

def spawnM(state, f, flags=[]):
	state = info(state, ["Spawning with flags", flags, "program", f])
	flags = set(flags)
	
	if Spawn.AWAIT in flags:
		flags.remove(Spawn.AWAIT)
		return must_spawn(state, f, flags)

	state, can = can_spawn(state)
	become = Spawn.BECOME in flags and not can
	if become:
		state, v = dos(state, [f])
		return state

	state, child_id = dos(state, [[next_child_id]])
	child_state = State.fork(state, child_id)
	#child_state["id"] = child_id
	#child_state = merge(state, {"id": child_id}, None, True)

	def spawn_inner():
		return dos(child_state, [f])

	child = spawn_drone(spawn_inner)
	if child == None:
		return error(state, ["Failed to spawn drone"])
	state["child_states"][child_id] = child_state
	state["child_handles"][child_id] = child
	return state

spawn = spawnM
	
def wait_for_child(state, child_id):
	child_state, v = wait_for(state["child_handles"][child_id])
	state["child_handles"].pop(child_id)
	state["child_states"].pop(child_id)
	return pure(state, (child_state, v))
	
def wait_all(state):
	vs = {}
	child_ids = []
	for child_id in state["child_handles"]:
		child_ids.append(child_id)
	for child_id in child_ids:
		state, (child_state, v) = wait_for_child(state, child_id)
		vs[child_id] = v
	return pure(state, vs)
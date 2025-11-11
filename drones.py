from lib import *
from debug import *
    
def update_drone_state(state):
    state["num_drones"] = num_drones()
    return unit(state)
    
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
        return spawn(state, f, flags)

    while not spawn(state, f)[1]:
        pass
    return pure(state, True)

def spawn_(state, f, flags=[]):
    return spawn(state, f, flags)[0]

def spawnM(state, f, flags=[]):
    state = info(state, ["Spawning with flags", flags, "program", f])
    flags = set(flags)
    
    if Spawn.AWAIT in flags:
        flags.remove(Spawn.AWAIT)
        return must_spawn(state, f, flags)

    state, can = can_spawn(state)
    become = Spawn.BECOME in flags and not can
    if become:
        return do_(state, [f])

    if Spawn.INHERIT in flags:
        child_state = State.fork(state)
    else:
        child_state = State.new(state["flags"])

    def spawn_inner():
        return dos(child_state, [f])

    child_state["id"] = num_drones()
    child = spawn_drone(spawn_inner)
    if child == None:
        return pure(state, False)
    state["child_states"][child_state["id"]] = child_state
    state["child_handles"][child_state["id"]] = child
    return pure(state, True)

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

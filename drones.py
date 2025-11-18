from lib import *
from debug import *
from excursion import *
from move import *
from Type import new
from State import State

def with_spawn_lock(state, f):
    state = Lock(state, "spawn")
    state = update_drone_state(state)
    state, x = f(state)
    state = Unlock(state, "spawn")
    return pure(state, x)

def only_drone(state):
    def p(state):
        return pure(state, state["num_drones"] == 1)
    return with_spawn_lock(state, p)

def update_drone_state(state):
    state = Lock(state, "spawn")
    state = Lock(state, "num_drones")
    state["num_drones"] = num_drones()
    state = Unlock(state, "num_drones")
    state = Unlock(state, "spawn")
    return state

def can_spawn(state):
    state = Lock(state, "can_spawn")
    state, can = do(state, [
        [update_drone_state],
        [pure, state["num_drones"] < state["max_drones"]]
    ])
    state = Unlock(state, "can_spawn")
    return pure(state, can)

def cond_spawn(state, f, g):
    state = Lock(state, "can_spawn")

    def do_return(state, h):
        state = Unlock(state, "can_spawn")
        return state.do([h])

    state, can = can_spawn(state)
    if can:
        return do_return(state, f)
    else:
        return do_return(state, g)

def spawn_(state, f, flags=[]):
    return spawn(state, f, flags).void()

def spawnM(state, f, flags=[]):
    state = info(state, ("Spawning with flags", flags, "program", f))
    flags = set(flags)

    state = Lock(state, "spawn")
    def do_return(state, value):
        state = Unlock(state, "spawn")
        return pure(state, value)

    if Spawn.BECOME in flags:
        state, became = state.cond_spawn(
            [pure, False],
            [do, [
                [Unlock, "spawn"],
                [when, Spawn.EXCURSE in flags, [start_excursion]],
                f,
                [when, Spawn.EXCURSE in flags, [end_excursion]],
                [pure, True]
            ]])
        if became:
            return do_return(state, True)

    if Spawn.AWAIT in flags:
        flags = without(flags, Spawn.AWAIT)
        state = Unlock(state, "spawn")
        spawned = False
        while not spawned:
            state, spawned = spawn(state, f, flags)
        return pure(state, spawned)

    state = Lock(state, "child_handles")

    child_id = state["id"] + len(state["child_handles"]) + 1
    if Spawn.CLONE in flags:
        child_state = dict(state)
        child_state["id"] = child_id
    elif Spawn.FORK in flags:
        state, child_state = state.fork(child_id)
    elif Spawn.SHARE in flags:
        state, child_state = state.share(child_id)
    elif Spawn.NEW in flags:
        child_state = State.new(state["flags"])
        child_state["id"] = child_id
    else:
        state = Unlock(state, "child_handles")
        state = Unlock(state, "spawn")
        return fatal(state, ("No Spawn flag provided", flags))

    if child_state["id"] in state["child_handles"]:
        state = Unlock(state, "child_handles")
        state = Unlock(state, "spawn")
        return fatal(state, ("Drone ID collision on spawn:",
                             child_state["id"],
                             "state:", state, "child_state:", child_state))

    def spawn_inner():
        return do(child_state, [f])

    spawned = False
    child = spawn_drone(spawn_inner)
    if child != None:
        spawned = True
        state["child_states"][child_state["id"]] = child_state
        state["child_handles"][child_state["id"]] = child

    state = Unlock(state, "child_handles")
    state = Unlock(state, "spawn")

    return pure(state, spawned)

spawn = spawnM

def wait_for_child(state, child_id):
    child_state, v = None, None

    if child_id in state["child_handles"]:
        child_state, v = wait_for(state["child_handles"][child_id])
        state = Lock(state, "child_handles")
        state["child_handles"].pop(child_id)
        state["child_states"].pop(child_id)
        state = Unlock(state, "child_handles")

    return pure(state, (child_state, v))

def wait_all(state):
    vs = {}
    child_ids = []
    for child_id in state["child_handles"]:
        if child_id != state["id"]:
            child_ids.append(child_id)

    for child_id in child_ids:
        state, (_, v) = wait_for_child(state, child_id)
        vs[child_id] = v

    return pure(state, vs)

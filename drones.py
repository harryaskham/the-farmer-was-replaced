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
    state = debug(state, ("Spawning with flags", flags, "program", f))
    flags = set(flags)

    state = Lock(state, "spawn")
    state = Lock(state, "child_handles")
    def do_return(state, value):
        state = Unlock(state, "child_handles")
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
        spawned = False
        while not spawned:
            state, spawned = spawn(state, f, flags)
        return do_return(state, spawned)

    state, child_id = get_next_id(state)

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
        state = fatal(state, ("No Spawn flag provided", flags))
        return do_return(state, None)

    if child_state["id"] in state["child_handles"]:
        state = fatal(
            state,
            ("Drone ID collision on spawn:", child_state["id"], "state:", state, "child_state:", child_state))
        return do_return(state, None)

    def after(child_state, r):
        def finalize(state):
            if Spawn.MERGE in flags:
                state = state.merge_state(child_state)

            state, _ = wait_all(state, child_state)

            state = Lock(state, "child_handles")
            state = Lock(state, "child_states")
            state = Lock(state, "drone_return")

            if child_state["id"] in state["child_states"]:
                state["child_states"].pop(child_state["id"])
            if child_state["id"] in state["child_handles"]:
                state["child_handles"].pop(child_state["id"])
            state["drone_return"][child_state["id"]] = r

            state = Unlock(state, "drone_return")
            state = Unlock(state, "child_states")
            state = Unlock(state, "child_handles")

            return pure(state, (child_state, r))
        return finalize

    def mk_spawn_inner(child_state):
        def spawn_inner():
            child_state_after, r = do(child_state, [f])
            finalize = after(child_state_after, r)
            return finalize
        return spawn_inner

    spawned = False
    child = spawn_drone(mk_spawn_inner(child_state))
    if child != None:
        spawned = True
        if Spawn.TRACK_STATE in flags:
            state["child_states"][child_state["id"]] = child_state
        state["child_handles"][child_state["id"]] = child

    return do_return(state, spawned)

spawn = spawnM

def wait_for_child_handle(state, child_handle):
    finalize = wait_for(child_handle)
    return finalize(state)

def wait_for_child(state, child_id, other_state=None):
    state = Lock(state, "child_handles")

    if other_state == None:
        other_state = state
    child_state, v = None, None
    if child_id in other_state["child_handles"]:
        state, (child_state, v) = wait_for_child_handle(state, other_state["child_handles"][child_id])
    else:
        if child_id in other_state["drone_return"]:
            v = other_state["drone_return"][child_id]
        if child_id in other_state["child_states"]:
            child_state = other_state["child_states"][child_id]
            state = state.merge_state(child_state)

    if child_id in state["child_handles"]:
        state["child_handles"].pop(child_id)
    if child_id in state["child_states"]:
        state["child_states"].pop(child_id)

    state = Unlock(state, "child_handles")
    return pure(state, (child_state, v))

def wait_all(state, other_state=None):
    if other_state == None:
        other_state = state
    vs = {}
    for child_id, handle in items(other_state["child_handles"]):
        state, (_, v) = wait_for_child(state, child_id, other_state)
        vs[child_id] = v

    return pure(state, vs)

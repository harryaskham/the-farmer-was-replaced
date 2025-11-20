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

DEFAULT_FLAGS = [
    Spawn.SHARE,
    Spawn.AWAIT,
]

def spawn_(state, f, flags=DEFAULT_FLAGS):
    return spawn(state, f, flags).void()

def spawnM(state, f, flags=DEFAULT_FLAGS):
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

    child_state["parent_id"] = state["id"]

    if child_state["id"] in state["child_handles"]:
        state = fatal(
            state,
            ("Drone ID collision on spawn:", child_state["id"], "state:", state, "child_state:", child_state))
        return do_return(state, None)

    def mk_spawn_inner(child_state):
        def spawn_inner():
            return do(child_state, [f])
        return spawn_inner

    spawned = False
    child = spawn_drone(mk_spawn_inner(child_state))
    if child != None:
        state = info(state, ("Spawned child drone", child_state["id"]))
        spawned = True
        state["child_handles"][child_state["id"]] = child

    return do_return(state, spawned)

spawn = spawnM

def wait_for_child(state, child_id):
    if child_id == state["id"]:
        return fatal(state, ("Cannot wait for self", child_id))

    if child_id == state["parent_id"]:
        return fatal(state, ("Cannot wait for parent", child_id))

    if child_id in state["child_returns"]:
        debug(state, ("Child already waited for", child_id))
        if child_id in state["child_states"]:
            return pure(state, (state["child_states"][child_id], state["child_returns"][child_id]))
        return pure(state, (None, state["child_returns"][child_id]))

    state = debug(state, ("Waiting for child", child_id))

    if child_id not in state["child_handles"]:
        return fatal(state, ("No such child handle", child_id))

    child_state, r = wait_for(state["child_handles"][child_id])

    state = merge_state(state, child_state)

    state["child_returns"][child_state["id"]] = r
    state["child_states"][child_state["id"]] = child_state

    for child_id in child_state["child_handles"]:
        wait_for_child(state, child_id)

    return pure(state, (child_state, r))

def wait_all(state):
    info(state, (len(state["child_handles"]), "handles", len(state["child_returns"]), "returns"))
    if len(state["child_handles"]) == len(state["child_returns"]):
        debug(state, ("All children have been waited for"))
        return state
    for child_id in keys(state["child_handles"]):
        state, _ = wait_for_child(state, child_id)
    return state

def wait_solo(state, delay_secs=1):
    while True:
        if num_drones() == 1:
            break
        wait_secs(delay_secs)
    return state

def wait_returns(state, delay_secs=1):
    while True:
        if len(state["child_handles"]) == len(state["child_returns"]):
            break
        wait_secs(delay_secs)
    return state

from lib import *
from debug import *
from excursion import *
from move import *
from Type import new
from State import *

def can_spawn(state):
    return pure(state, num_drones() < max_drones())

DEFAULT_FLAGS = [
    Spawn.FORK,
    Spawn.BECOME,
]

NOT_STARTED = "NOT_STARTED"
STARTED = "STARTED"
BECAME = "BECAME"
FINISHED = "FINISHED"
MERGED_SELF = "MERGED_SELF"
MERGED_CHILDREN = "MERGED_CHILDREN"

def Handle(status, child_id, handle=None):
    return {
        "child_id": child_id,
        "status": status,
        "handle": handle,
    }

def spawn_(state, f, flags=DEFAULT_FLAGS):
    return spawn(state, f, flags).void()

def mk_spawn_inner(child_state, f):
    def spawn_inner():
        return do(child_state, [f])
    return spawn_inner

def spawn(state, f, flags=DEFAULT_FLAGS):
    return spawns(state, [f], flags)

def replicate(state, f, n, flags=DEFAULT_FLAGS):
    fs = []
    for _ in range(n):
        fs.append(f)
    return spawns(state, fs, flags)

def spawns(state, fs, flags=DEFAULT_FLAGS):
    flags = set(flags)
    states = {}
    handles = {}
    spawn_fs = {}
    for f in fs:
        state = debug(state, ("Spawning with flags", flags, "program", f))

        state, child_id = get_next_id(state)
        if Spawn.CLONE in flags:
            child_state = dict(state)
            child_state["id"] = child_id
        elif Spawn.FORK in flags:
            child_state = fork(state, child_id)
            child_state["id"] = child_id
        elif Spawn.SHARE in flags:
            child_state = share(state, child_id)
            child_state["id"] = child_id
        elif Spawn.NEW in flags:
            child_state = State.new(state["flags"])
            child_state["id"] = child_id
            for k in ["maze"]:
                child_state[k] = dict(state[k])
        else:
            return fatal(state, ("No Spawn flag provided", flags))

        state = debug(state, ("Child state created: parent", state["id"], "child", child_id))
        child_state["parent_id"] = state["id"]

        if child_id in state["child_handles"] or child_id in handles:
            return fatal(
                state,
                ("Drone ID collision on spawn:", child_state["id"], "state:", state, "child_state:", child_state))

        states[child_id] = child_state
        handles[child_id] = Handle(NOT_STARTED, child_id)
        spawn_fs[child_id] = mk_spawn_inner(child_state, f)

    for child_id, handle in handles.items():
        state["child_handles"][child_id] = handle
        #state["child_states"][child_id] = states[child_id]

    for child_id in handles:
        spawn_f = spawn_fs[child_id]
        child_state = states[child_id]
        while True:
            child = spawn_drone(spawn_f)
            if child != None:
                state = info(state, ("Parent drone", state["id"], "spawned child drone", child_state["id"]))
                state["child_handles"][child_id] = Handle(STARTED, child_id, child)
                break
            elif Spawn.BECOME in flags:
                state = info(state, ("Parent drone", state["id"], "becoming child drone", child_state["id"]))
                state = become(state, child_state, f)
                state = info(state, ("Parent drone", state["id"], "became child drone", child_state["id"]))
                break
            else:
                state = info(state, ("Parent drone", state["id"], "failed to spawn child drone", child_state["id"], "retrying"))
                wait_secs(1)

    #return wait_all(state, True)
    return pure(state, True)

def wait_for_child(state, child_id, recursive=True):
    if child_id == state["id"]:
        return fatal(state, ("Cannot wait for self", child_id))

    if child_id == state["parent_id"]:
        return fatal(state, ("Cannot wait for parent", child_id))

    child_state = None
    r = None

    #if child_id in state["child_returns"]:
    #    debug(state, ("Child already waited for", child_id))
    #    if child_id in state["child_states"]:
    #        return pure(state, (state["child_states"][child_id], state["child_returns"][child_id], waited))
    #    return pure(state, (None, state["child_returns"][child_id], waited))

    if child_id not in state["child_handles"]:
        return fatal(state, ("No such child handle", child_id))

    handle = state["child_handles"][child_id]
    state = info(state, (state["id"], "waiting for handle:", handle))
    if handle["status"] == BECAME:
        state = debug(state, ("Not waiting for BECAME child", child_id))
        return pure(state, (state, None))

    if handle["status"] in [NOT_STARTED]:
        state = debug(state, ("Not waiting for unstarted child", child_id))
        return pure(state, None)

    if handle["status"] in [STARTED, FINISHED]:
        state = debug(state, ("Waiting for child with status", handle["status"], child_id))
        child_state, r = wait_for(handle["handle"])
        state["child_returns"][child_state["id"]] = r
        #state["child_states"][child_state["id"]] = child_state
        info(state, ("Child drone returned", child_id, "return value", r, "child state", child_state["maze"]))
        handle["status"] = FINISHED

    if handle["status"] == FINISHED:
        state = debug(state, ("Merging child with status", handle["status"], child_id))
        state = merge_state(state, child_state)
        handle["status"] = MERGED_SELF

    if (handle["status"] == MERGED_SELF) and recursive:
        child_state, _ = wait_all(child_state, recursive)
        state = merge_state(state, child_state)
        handle["status"] = MERGED_CHILDREN

    if (
        (recursive and (handle["status"] == MERGED_CHILDREN))
        or (not recursive and (handle["status"] == MERGED_SELF))
    ):
        return pure(state, (child_state, r))

    return fatal(state, ("Unhandled handle status in wait_for_child", handle["status"], child_id))

def wait_all(state, recursive=True):
    ks = keys(state["child_handles"])
    n_children = len(ks)
    any_remaining = False

    for child_id in ks:
        state, out = wait_for_child(state, child_id, recursive)
        any_remaining = any_remaining or (out == None)

    ks = keys(state["child_handles"])
    if any_remaining or n_children != len(ks):
        return wait_all(state, recursive)

    for handle in values(state["child_handles"]):
        if (
            (recursive and handle["status"] != MERGED_CHILDREN)
            or (not recursive and handle["status"] != MERGED_SELF)
        ):
            return wait_all(state, recursive)

    state["child_handles"] = {}
    return pure(state, True)

def wait_solo(state, delay_secs=1):
    while True:
        if num_drones() == 1:
            break
        wait_secs(delay_secs)
    return state

def wait_all_solo(state, recursive=True, delay_secs=1):
    return state.do([
        [wait_solo, delay_secs],
        [wait_all, recursive],
    ])

def wait_returns(state, delay_secs=1):
    while True:
        quick_print(state["id"], state["child_handles"], len(state["child_returns"]))
        if len(state["child_handles"]) == len(state["child_returns"]):
            break
        wait_secs(delay_secs)
    return state

def become(state, child_state, f):
    child_id = child_state["id"]
    state["child_handles"][child_id] = Handle(BECAME, child_id)
    #state["child_states"][child_id] = child_state
    child_state, r = child_state.do([
        [start_excursion],
        f,
    ])
    child_state = child_state.do_([
        [end_excursion]
    ])
    state["child_returns"][child_id] = r
    state["child_handles"][child_id] = Handle(FINISHED, child_id)
    return state

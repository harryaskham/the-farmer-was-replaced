from debug import *
from monad import *
from time import *

def delay_lock(state, conditionM, actionM, delay=None):
    if delay == None:
        delay = state["delay"]
    state, c = state.do([conditionM])
    if c:
        if delay > 0:
            state = state.do_([[wait_secsM, delay]])
        state, c = state.do([conditionM])
        if c:
            state = state.do_([actionM])
    return pure(state, c)

def lines(state, level, msgs):
    state = Lock(state, "locking.lines")
    state = log_drone_info(state, level)
    for msg in msgs:
        state = log(state, msg, level, None, True)
    return Unlock(state, "locking.lines")
    return state

def all_states(state):
    states = [state]
    for other in states["child_states"]:
        states.append(other)
    return states

def Metalocks(state, retry_delay=0.1):
    locked_ids = set()
    while True:
        for other in all_states(state):
            if other["id"] in locked_ids:
                continue
            _, locked = Metalock(other, state["id"])
            if locked:
                locked_ids.add(other["id"])

        if len(locked_ids) < len(states):
            wait_secs(retry_delay)
            continue

        return pure(state, True)

def Metalock(state, id=None):
    if id == None:
        id = state["id"]

    if state["locks"]["__locked__"]:
        verbose(state, ("Drone", id, "waiting for global lock"))
        wait_secs(0.1)
        return pure(state, False)

    state["locks"]["__locked__"] = True
    state["locks"]["__lockers__"].add(id)

    if len(state["locks"]["__lockers__"]) > 1:
        state["locks"]["__lockers__"].remove(id)
        state = fatal(state, ("Multiple lockers at once:", state["locks"]["__lockers__"]))

    return pure(state, True)

def Metaunlock(state, id=None):
    if id == None:
        id = state["id"]
    state["locks"]["__lockers__"].remove(id)
    state["locks"]["__locked__"] = False
    return state

def Metaunlocks(state):
    for other in all_states(state):
        Metaunlock(other, state["id"])
    return state

def Lock(state, key, reentrant=True, retry_delay=0.1):
    return state

def Lock_(state, key, reentrant=True, retry_delay=0.1):
    locked = False
    while True:
        state, locked = TryLock(state, key, reentrant)
        if locked:
            break
        wait_secs(retry_delay)
    return state

def TryLock(state, key, reentrant=True):
    state, locked = Metalock(state)
    if not locked:
        return pure(state, False)

    locks = state["locks"]
    success = False
    if key not in locks:
        locks[key] = [state["id"], 1]
        verbose(state, ("Drone", state["id"], "acquired new lock", key, locks[key]))
        success = True
    elif locks[key][0] == None:
        verbose(state, ("Drone", state["id"], "acquired existing lock", key, locks[key]))
        locks[key][0] = state["id"]
        locks[key][1] = 1
        success = True
    elif locks[key][0] == state["id"] and reentrant:
        verbose(state, ("Drone", state["id"], "already has lock, incrementing", key, locks[key]))
        locks[key][1] += 1
        success = True
    else:
        state = verbose(state, ("Drone", state["id"], "waiting for lock", key, locks[key]))
        success = False

    state = Metaunlock(state)
    return pure(state, success)

def Unlock(state, key, retry_delay=0.1):
    return state

def Unlock_(state, key, retry_delay=0.1):
    unlocked = False
    while True:
        state, unlocked = TryUnlock(state, key)
        if unlocked:
            break
        wait_secs(retry_delay)
    return state

def TryUnlock(state, key):
    state, locked = Metalock(state)
    if not locked:
        return pure(state, False)

    locks = state["locks"]
    if key not in locks:
        state = fatal(state, ("Lock", key, "never locked by any drone"))
    elif locks[key][0] == None:
        state = fatal(state, ("Lock", key, "not held by any drone"))
    elif locks[key][0] != state["id"]:
        state = fatal(state, ("Lock", key, "held by other drone:", locks[key]))
    else:
        verbose(state, ("Drone", state["id"], "released lock", key, locks[key]))
        if locks[key][1] == 1:
            locks[key][0] = None
            locks[key][1] = None
            verbose(state, ("Drone", state["id"], "released lock", key, locks[key]))
        else:
            locks[key][1] -= 1
            verbose(state, ("Drone", state["id"], "decremented lock", key, locks[key]))

    state = Metaunlock(state)
    return pure(state, True)

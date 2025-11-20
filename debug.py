from flags import *
from aliases import *
from error import *
from strings import *
from builtin_types import *

def log_drone_info(state, level):
    return log(
        state,
        join([str(level), state["id"], str((state["x"], state["y"])), str(num_drones())], " | "),
        level,
        None,
        True)

def log(state, msg, level=Log.DEBUG, prefix=None, hide_drone_info=False):

    if Log.EXCLUSIVE in state["flags"]:
        state = Lock(state, "log", False)
        def do_return(state):
            state = Unlock(state, "log")
            return state
    else:
        def do_return(state):
            return state

    if (ONLY_LOG_DRONES != None) and (state["id"] not in ONLY_LOG_DRONES):
        return do_return(state)

    debug_level = 0
    for l in Log.Levels:
        if l in state["flags"]:
            debug_level = max(debug_level, Log.Levels[l])
    
    if level in Log.Levels:
        n_level = Log.Levels[level]
    else:
        n_level = level

    if n_level > debug_level:
        return do_return(state)
        
    if prefix != None:
        msg = prefix + " " + str(msg)
    
    if Log.AIR in state["flags"]:
        print(msg)

    if (level != Log.TRACE) and (Log.DRONE_DETAILS in state["flags"]) and (not hide_drone_info):
        state = log_drone_info(state, level)

    if Log.REPR in state["flags"]:
        msgs = []
        if of(msg) in [List, Tuple]:
            msgs = list(msg)
        else:
            msgs = [msg]
        fmsgs = []
        for msg in msgs:
            fmsgs.append(repr(msg))
        if Log.SHOW_LEVEL in state["flags"]:
            quick_print([level, join(fmsgs, " ")])
        else:
            quick_print(join(fmsgs, " "))
    else:
        if Log.SHOW_LEVEL in state["flags"]:
            quick_print([level, msg])
        else:
            quick_print(msg)

    return do_return(state)

def info(state, msg):
    return log(state, msg, Log.INFO)
    
def debug(state, msg, unused=None, prefix=None):
    return log(state, msg, Log.DEBUG, prefix)

def trace(state, msg):
    return log(state, msg, Log.TRACE)

def warn(state, msg):
    return log(state, msg, Log.WARN)
    
def error(state, msg, level=Log.ERROR):
    state = throw(state, msg)
    return log(state, msg, level)
    
def fatal(state, msg):
    state = error(state, msg, Log.FATAL)
    return terminate(state)
    
def verbose(state, msg, prefix=None):
    return log(state, msg, Log.VERBOSE, prefix)
    
def shim_state():
    flags = set(MAIN_FLAGS)
    if Log.DRONE_DETAILS in flags:
        flags.remove(Log.DRONE_DETAILS)
    state = {
        "__type__": {"name": "State"},
        "flags": flags,
        "id": "1",
        "x": "_",
        "y": "_",
        "error": None,
        "locks": {
            "__locked__": False,
            "__lockers__": set()
        }
    }
    return state
    
def info_(msg):
    return info(shim_state(), msg)
    
def debug_(msg):
    return debug(shim_state(), msg)

def verbose_(msg):
    return verbose(shim_state(), msg)
    
def warn_(msg):
    return warn(shim_state(), msg)

def trace_(msg):
    return trace(shim_state(), msg)
    
def error_(msg):
    return error(shim_state(), msg)
    
def fatal_(msg):
    return fatal(shim_state(), msg)

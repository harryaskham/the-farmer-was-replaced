from terminate import *

def throw(state, msg):
    state["error"] = msg
    return state
    
def catch(state, f):
    e = state["error"]
    if e == None:
        return state
    state["error"] = None
    return apply(state, f, [e])
    
def has_error(state):
    return pure(state, state["error"] != None)


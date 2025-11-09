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

def terminate(state):
    quick_print("Terminating with state:")
    quick_print(state)
    return terminate_()
    
def terminate_():
    quick_print("Terminating")
    return TERMINATE

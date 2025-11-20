from debug import *

def trace_id(state, level, prefix, x):
    state = log(state, x, level, "[trace] " + prefix)
    return x

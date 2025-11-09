from debug import *

def trace(state, level, prefix, x):
    state = debug(state, x, level, "[trace] " + prefix)
    return x
from debug import *
from monad import *

def trace_id(state, level, prefix, x):
    state = log(state, x, level, "[trace] " + prefix)
    return x

def traceM(ma, level=Log.INFO, prefix=""):
    return [bind, ma, [trace_id, level, prefix]]

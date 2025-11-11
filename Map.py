from operators import *
from monad import *

def from_list(kvs):
    xs = {}
    for k, v in kvs:
        xs[k] = v
    return xs

def mapM_(state, f, xs):
    return dos_(state, [mapM, f, values(xs)])

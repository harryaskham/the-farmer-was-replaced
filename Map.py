from operators import *
import monad
from dict import *
from monad import do, fmap, traverse
import List
import dict

def from_list(kvs):
    xs = {}
    for k, v in kvs:
        xs[k] = v
    return xs

to_list = items

def bimap(f, g, xs):
    ys = {}
    for a, b in xs.to_list():
        ys[f(a)] = g(b)
    return ys

def mapM(state, f, xs):
    return do(state, [
        [monad.mapM, f, values(xs)]
    ])

def mapM_(state, f, xs):
    return mapM(state, f, xs).void()

def bimapM(state, f, g, xs):
    return state.do([
        [fmap,
            [from_list],
            [traverse, [monad.bimapM, f, g], to_list(xs)]]
    ])

values = dict.values
keys = dict.keys
items = dict.items

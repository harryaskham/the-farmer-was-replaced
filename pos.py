from monad import *
from aliases import *
from locking import *
from cell import mk_cell_state
from operators import flipM
import test

def top_right(state):
    state, d = wh(state)
    return pure(state, (d - 1, d - 1))

def box(state):
    state, d = wh(state)
    return pure(state, [0, 0, d, d])

def row_box(d, y):
    return [0, y, d, 1]

def x(state):
    return pure(state, state["x"])
    
def y(state):
    return pure(state, state["y"])
    
def xy(state):
    state, sx = x(state)
    state, sy = y(state)
    return pure(state, (sx, sy))

def wh(state):
    return pure(state, state["wh"])

def et(state):
    return get_here(state, "entity_type")
    
def gt(state):
    return get_here(state, "ground_type")

def get_to(state, dir, key=None):
    return dos(state, [
        [bind, [pos_to, dir], [flipM, get_at, key]]
    ])
        

def at(state, c):
    if c == None:
        return pure(state, None)
    x, y = unpack(c)
    if (x, y) in state["grid"]:
        return pure(state, state["grid"][(x, y)])
    cell = mk_cell_state(x, y)
    state["grid"][(x, y)] = cell
    return pure(state, cell)
        
def here(state):
    state, c = xy(state)
    return at(state, c)

def exists_to(state, dir):
    state, p = pos_to(state, dir)
    return pure(state, p != None)

def get_at(state, c, key=None):
    if c == None:
        return pure(state, None)

    if key == None:
        return at(state, c)

    state, xs = at(state, c)

    if xs == None or key not in xs:
        return pure(state, None)

    return pure(state, xs[key])

def set_at(state, c, fields, flags=[]):
    this_state = state
    flags = set(flags)
    x, y = unpack(c)
    states = [state]
    if To.CHILDREN in flags:
        for child_id in state["child_states"]:
            child_state = state["child_states"][child_id]
            states.append(child_state)

    for state in states:
        if (x, y) not in state["grid"]:
            if (x, y) in this_state["grid"]:
                state["grid"][(x, y)] = mk_cell_state(x, y, this_state["grid"][(x, y)])
            else:
                state["grid"][(x, y)] = mk_cell_state(x, y)
                
        state["grid"][(x, y)] = merge(state["grid"][(x, y)], fields, None, Copy.CELL in flags)

    return states[0]

def get_here(state, key=None):
    state, c = xy(state)
    return get_at(state, c, key)
    
def set_here(state, fields, flags=[]):
    state, c = xy(state)
    return set_at(state, c, fields, flags)
    
def opposite(d):
    return {
        North: South,
        South: North,
        East: West,
        West: East
    }[d]

def i2(state, id=None):
    if id == None:
        id = state["id"]
    return pure(state, id % 2 == 0)

def ixy(state, id=None):
    if id == None:
        id = state["id"]
    state, d = wh(state)
    y = 0
    while id >= d:
        id -= d
        y += 1
    x = id
    return pure(state, (x, y))
    
def pos_to(state, dir, c=None):
    if c == None:
        state, c = xy(state)
    x, y = unpack(c)
    state, d = wh(state)
    if dir == North and y < d - 1:
        return pure(state, (x, y+1))
    if dir == South and y > 0:
        return pure(state, (x, y-1))
    if dir == East and x < d - 1:
        return pure(state, (x+1, y))
    if dir == West and x > 0:
        return pure(state, (x-1, y))
    return unit(state)

def with_cell(state, c, f):
    state = Lock(state, ("cell", c))

    state, result = dos(state, [
        [bind, [get_at, c], [f]]
    ])

    state = Unlock(state, ("cell", c))
    return pure(state, result)

def with_here(state, f):
    return with_cell(state, (state["x"], state["y"]), f)

def with_et(state, f):
    def g(state, cell):
        return f(state, cell["entity_type"])
    return with_here(state, g)

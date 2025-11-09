from monad import *
from aliases import *
from cell import mk_cell_state

def top_right(state):
    state, d = wh(state)
    return pure(state, (d - 1, d - 1))

def box(state):
    state, d = wh(state)
    return pure(state, [0, 0, d, d])

def x(state):
    return pure(state, state["x"])
    
def y(state):
    return pure(state, state["y"])
    
def xy(state):
    state, sx = x(state)
    state, sy = y(state)
    return pure(state, [sx, sy])

def xy_tup(state):
    state, [x, y] = xy(state)
    return pure(state, (x, y))
    
def wh(state):
    return pure(state, state["wh"])

def et(state):
    return get_here(state, "entity_type")
    
def gt(state):
    return get_here(state, "ground_type")

def get_to(state, dir, key=None):
    return dos(state, [
        [bind, [pos_to, dir], [flipM, [get_at, key]]]
    ])
        

def at(state, c):
    x, y = unpack(c)
    if (x, y) in state["grid"]:
        return pure(state, state["grid"][(x, y)])
    cell = mk_cell_state(x, y)
    state["grid"][(x, y)] = cell
    return pure(state, cell)
        
def here(state):
    state, c = xy(state)
    return at(state, c)
    
def get_at(state, c, key=None):
    if key == None:
        return at(state, c)
    else:
        state, xs = at(state, c)
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
                state["grid"][(x, y)] = this_state["grid"][(x, y)]
            else:
                state["grid"][(x, y)] = mk_cell_state(x, y)
                
        if Copy.CELL in flags:
            state["grid"][(x, y)] = merge(state["grid"][(x, y)], fields)
        else:
            for k in fields:
                state["grid"][(x, y)][k] = fields[k]
    
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
    
def pos_to(state, d, c=None):
    if c == None:
        state, c = xy(state)
    x, y = unpack(c)
    state, d = wh(state)
    if d == North and y < d - 1:
        return pure(state, [x, y+1])
    if d == South and y > 0:
        return pure(state, [x, y-1])
    if d == East and x < d - 1:
        return pure(state, [x+1, y])
    if d == West and x > 0:
        return pure(state, [x-1, y])
    return unit(state)

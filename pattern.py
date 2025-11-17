from lib import *
from planting import *

def Box(state, x, y, box, f=[], g=[]):
    [x0, y0, w, h] = box
    b0 = x >= x0 and y >= y0
    b1 = x < x0 + w and y < y0 + h
    if b0 and b1:
        return do(state, [f])
    else:
        return do(state, [g])

def Patch(state, x, y, x0, y0, size, f=[], g=[]):
    return Box(state, x, y, [x0, y0, x0 + size, y0 + size], f, g)

def Checker(state, x, y, f=[unit], g=[unit]):
    if (x + y) % 2 == 0:
        return do(state, [f])
    else:
        return do(state, [g])

def Checker3(state, f=[unit], g=[unit], h=[unit]):
    state, (x, y) = xy(state)
    m = (x + y) % 3
    if m == 0:
        return do(state, [f])
    elif m == 1:
        return do(state, [g])
    else:
        return do(state, [h])

def Checker0(state, f):
    state, (x, y) = xy(state)
    return Checker(state, x, y, f, [unit])

def Checker1(state, g):
    state, (x, y) = xy(state)
    return Checker(state, x, y, [unit], g)

def Companion_(state, flags=[]):
    return Companion(state, [unit], flags)

def Companion(state, otherwise=[unit], flags=[]):
    state, c = get_here(state, "companion")
    return do(state, [
        [cond, c == None,
            otherwise,
            [plantM, c, flags]
        ]
    ])

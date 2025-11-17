from lib import *
from move import *

def traverse_farm(state, f, box=None, start=None, reverse=False, flags=[]):
    state, d = wh(state)

    if box == None:
        box = [0, 0, d-1, d-1]

    if start == None:
        start = box[:2]

    state = move_to(state, start, flags)

    res = {}
    for yi in range(box[3]):
        if reverse:
            y = (start[1] - yi) % d
        else:
            y = (start[1] + yi) % d

        for xi in range(box[2]):
            if reverse:
                x = (start[0] - xi) % d
            else:
                x = (start[0] + xi) % d

            state = move_to(state, (x, y))
            xss = f(state, x, y)
            state, out = do(state, xss)
            res[(x, y)] = out
    return state, res

def box_do(state, box, f, flags=[]):
    flags = set(flags)
    loop = Movement.LOOP in flags
    reverse = Movement.REVERSE in flags
    if reverse:
        start = corner(box, NE)
    else:
        start = corner(box, SW)
    return boxloop(state, box, f, start, loop, reverse, flags)

def boxloop(state, box, f, start=None, loop=True, reverse=False, flags=[]):
    def g(state, x, y):
        return [f]
    return farmloop(state, g, loop, False, box, start, reverse, flags)

def farmloop(state, f, loop=True, scan=False, box=None, start=None, reverse=False, flags=[]):
    if scan:
        state, out = traverse_farm(state, nop3, box, start, reverse, flags)

    def go(state):
        return traverse_farm(state, f, box, start, reverse, flags)

    while True:
        state, out = go(state)
        state["i"] += 1
        if not loop:
            return state, out

from lib import *
from harvest import *
from pattern import *
from planting import *
from measure import *
from sense import *
    
def neighbor_to(state, d):
    state, c = xy(state)
    state, n = pos_to(state, d, c)
    return pure(state, n)

def swap_key(a, b, key):
    ax = a[key]
    a[key] = b[key]
    b[key] = ax

def swapM(state, d):
    state, this = here(state)
    state, that = neighbor_to(state, d)
    if that == None:
        return pure(state, False)
    swap(d)
    return pure(state, True)

def ordinal_neighbors(state):
    state, (x, y) = xy(state)
    return pure(state, {
        West: get_at(state, [x-1,y])[1],
        South: get_at(state, [x,y-1])[1],
        East: get_at(state, [x+1,y])[1],
        North: get_at(state, [x,y+1])[1]
    })
    
def swap_if(d, a, b):
    if not ("cactus_size" in a and "cactus_size" in b):
        return None
    ca = a["cactus_size"]
    cb = b["cactus_size"]
    if ca == None or cb == None:
        return None
    return {
        West: ca < cb,
        South: ca < cb,
        East: ca > cb,
        North: ca > cb
    }[d]

def swap_once(state, dirs=None):
    if dirs == None:
        dirs = list(Dirs)

    state = sense(state, [Sensing.DIRECTIONAL])
    state, (x, y) = xy(state)
    state, this = here(state)
    state, ns = ordinal_neighbors(state)

    swapped = False
    for d in dirs:
        if d not in ns:
            continue

        n = ns[d]
        if n == None:
            continue

        cmp = swap_if(d, this, n)
        state = info(state, ((x, y), d, this["cactus_size"], n["cactus_size"], cmp))
        if cmp == True:
            state, swapped = swapM(state, d)
            if swapped:
                break

    return pure(state, swapped)

def emplace_once(state, dirs=None):
    if dirs == None:
        dirs = list(Dirs)

    def go(state):
        done = False
        moved = False
        i = -1
        while not done:
            i += 1
            if i > 100:
                break
            state = sense(state, [Sensing.DIRECTIONAL])
            state, (x, y) = xy(state)
            state, this = here(state)
            state, ns = ordinal_neighbors(state)

            done = True
            for d in dirs:
                if d not in ns:
                    continue

                n = ns[d]
                if n == None:
                    continue

                cmp = swap_if(d, this, n)
                state = info(state, ((x, y), d, this["cactus_size"], n["cactus_size"], cmp))
                if cmp == True:
                    state, swapped = swapM(state, d)
                    if swapped:
                        state, moved = moveM(state, d)
                        if moved:
                            done = False
                            break

        if moved:
            return go(state)
        return pure(state, moved)

    state, start = xy(state)
    state, moved = go(state)
    state = move_to(state, start)
    return pure(state, moved)

def emplace_cactus(state, dirs=None):
    done = False
    moved = False
    while not done:
        state, moved_now = emplace_once(state, dirs)
        if moved_now:
            moved = True
            continue
        if not moved_now:
            done = True
            break
    return pure(state, moved)

def Cactus(state, x, y, box, otherwise):
    def do_harvest(state):
        state, c = xy(state)
        if c == corner(box, SW):
            state = try_harvest(state, [E.Cactus])
            state = set_box_harvested(state, box)
        return state
        
    return do(state, [
        [Box, x, y, box,
            [dos, [
                [do_harvest],
                [plant_one, E.Cactus],
                [emplace_cactus]
            ]],
            otherwise
        ]
    ])

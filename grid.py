from lib import *
from pos import *
from cell import *
from locking import *

NE = [North, East]
NW = [North, West]
SE = [South, East]
SW = [South, West]

def coords(box):
    cs = []
    [x0, y0, w, h] = box
    for x in range(x0, x0+w):
        for y in range(y0, y0+h):
            cs.append((x, y))
    return cs
    
def corner(box, dir):
    [x0, y0, w, h] = box
    if dir == NE:
        return [x0+w-1, y0+h-1]
    if dir == SW:
        return [x0, y0]

    
def neighbors(state, cx=None, cy=None):
    state, d = wh(state)
    if cx == None:
        state, cx = x(state)
    if cy == None:
        state, cy = y(state)
    ns = []
    if cx > 0:
        ns.append((cx-1, cy))
    if cx < d - 1:
        ns.append((cx+1, cy))
    if cy > 0:
        ns.append((cx, cy-1))
    if cy < d - 1:
        ns.append((cx, cy+1))
    return pure(state, ns)
    
def neighbors_dict(state, cx=None, cy=None):
    state, d = wh(state)
    if cx == None:
        state, cx = x(state)
    if cy == None:
        state, cy = y(state)
    ns = {}
    if cx > 0:
        ns[West] = (cx-1, cy)
    if cx < d - 1:
        ns[East] = (cx+1, cy)
    if cy > 0:
        ns[South] = (cx, cy-1)
    if cy < d - 1:
        ns[North] = (cx, cy+1)
    return pure(state, ns)

def print_grid(state, level=Log.INFO):
    d = get_world_size()
    rows = [""]
    for k in ["id", "petal_counts"]:
        rows.append(join([k, " = ", str(state[k])]))
    for y in range(d):
        rows.append(print_row(state, y, d))
    return lines(state, level, rows)

def print_row(state, y, d):
    row = []
    for x in range(d):
        row.append(print_cell(state, (x, d - y - 1)))
    return join(row)

def print_cell(state, c):
    if c not in state["grid"]:
        return "? "
    def print_sunflower():
        if state["grid"][c]["petals"] == None:
            return "s?"
        return "s" + str(state["grid"][c]["petals"] - 7)

    return {
        None: ". ",
        E.Grass: "g ",
        E.Bush: "b ",
        E.Tree: "t ",
        E.Carrot: "c ",
        E.Sunflower: print_sunflower(),
        E.Cactus: "c ",
        E.Pumpkin: "p ",
        E.Dead_Pumpkin: "px",
        E.Hedge: "h ",
        E.Treasure: "$ ",
        E.Apple: "A ",
    }[state["grid"][c]["entity_type"]]

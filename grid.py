from lib import *
from pos import *
from cell import *

NE = [North, East]
NW = [North, West]
SE = [South, East]
SW = [South, West]

def mk_grid(cell=None):
	grid = []
	d = get_world_size()
	for y in range(d):
		row = []
		for x in range(d):
			row.append(mk_cell_state(x, y))

		grid.append(row)
	return grid

def coords(box):
	cs = []
	[x0, y0, w, h] = box
	for x in range(x0, x0+w):
		for y in range(y0, y0+h):
			cs.append([x, y])
	return cs
	
def get2d(g, c):
	[x, y] = c
	return g[y][x]
	
def set2d(g, c, k, v):
	[x, y] = c
	g[y][x][k] = v
	
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
		ns.append([cx-1, cy])
	if cx < d - 1:
		ns.append([cx+1, cy])
	if cy > 0:
		ns.append([cx, cy-1])
	if cy < d - 1:
		ns.append([cx, cy+1])
	return ns
	
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
	return ns
	
def get_row(state, y):
	return pure(state, state["grid"][y])

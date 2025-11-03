from lib import *
from harvest import *
from pattern import *
from planting import *
from measure import *
from sense import *
from move import *
	
def pos_to(state, d, c):
	[x, y] = c
	if d == North and y < wh(state) - 1:
		return [x, y+1]
	if d == South and y > 0:
		return [x, y-1]
	if d == East and x < wh(state) - 1:
		return [x+1, y]
	if d == West and x > 0:
		return [x-1, y]
	return None
	
def neighbor_to(state, d):
	return dos(state, [
		[then,
			[at],
			[bind, [xy], [pos_to, d]],
		]
	])

def swap_key(a, b, key):
	ax = a[key]
	a[key] = b[key]
	b[key] = ax

def swapM(state, d):
	this = here(state)
	that = neighbor_to(state, d)
	if that == None:
		return state
	swap(d)
	swap_key(this, that, "x")
	swap_key(this, that, "y")
	swap_key(this, that, "ground_type")
	state["grid"][that["y"]][that["x"]] = that
	state["grid"][this["y"]][this["x"]] = this	
	return state

	
def ordinal_neighbors(state):
	[x, y] = xy(state)
	return {
		West: get_at(state, [x-1,y]),
		South: get_at(state, [x,y-1]),
		East: get_at(state, [x+1,y]),
		North: get_at(state, [x,y+1])
	}
	
def cactus_cmp(d, a, b):
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
	}

def emplace_cactus(state, box, path=[]):
	while True:
		[x, y] = xy(state)
		this = here(state)
		ns = ordinal_neighbors(state)
		moved = False
		for d in [South, West]:
			if d not in ns:
				continue
			n = ns[d]
			if n == None:
				continue
			cmp = cactus_cmp(d, this, n)
			if cmp == None or not cmp[d]:
				continue

			moved = True
			state = swapM(state, d)
			state = moveM(state, d)
			state = sense(state, False)
			path.append(opposite(d))
			break
			
		if moved:
			continue
				
		if path == []:
			return state
			
		while path != []:
			d = path.pop()
			state = moveM(state, d)
			state = sense(state)


def Cactus(state, x, y, box, otherwise):
	def do_harvest(state):
		if xy(state) == corner(box, NE):
			state = try_harvest(state, [E.Cactus])
			state = set_box_harvested(state, box)
		return state
		
	return dos(state, [
		[Box, x, y, box,
			[dos, [
				[plant_one, E.Cactus],
				[sense, True],
				[emplace_cactus, box],
				[do_harvest]
			]],
			otherwise
		]
	])
from lib import *
from harvest import *
from pattern import *
from planting import *
from measure import *
from sense import *
	
def pos_to(state, d, c):
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
		return state
	swap(d)
	swap_key(this, that, "x")
	swap_key(this, that, "y")
	swap_key(this, that, "ground_type")
	state["grid"][that["y"]][that["x"]] = that
	state["grid"][this["y"]][this["x"]] = this	
	return sense(state)

	
def ordinal_neighbors(state):
	state, [x, y] = xy(state)
	return pure(state, {
		West: get_at(state, [x-1,y])[1],
		South: get_at(state, [x,y-1])[1],
		East: get_at(state, [x+1,y])[1],
		North: get_at(state, [x,y+1])[1]
	})
	
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

def emplace_cactus(state, dirs=list(Dirs)):
	state = start_excursion(state)
	moved = True
	while moved:
		state = sense(state)
		state, [x, y] = xy(state)
		state, this = here(state)
		state, ns = ordinal_neighbors(state)
		moved = False
		for d in dirs:
			if d not in ns:
				continue
				
			n = ns[d]
			if n == None:
				continue
				
			cmp = cactus_cmp(d, this, n)
			if cmp == None or not cmp[d]:
				continue

			state = info(state, (x, y, d, cmp))
			moved = True
			state = swapM(state, d)
			state = moveM(state, d)
			break
	state, excursion = current_excursion(state)
	did_sort = excursion != []
	state = end_excursion(state)
	return pure(state, did_sort)

def Cactus(state, x, y, box, otherwise):
	def do_harvest(state):
		state, c = xy(state)
		if c == corner(box, SW):
			state = try_harvest(state, [E.Cactus])
			state = set_box_harvested(state, box)
		return state
		
	return dos(state, [
		[Box, x, y, box,
			[dos, [
				[do_harvest],
				[plant_one, E.Cactus],
				[sense, True],
				[emplace_cactus, box]
			]],
			otherwise
		]
	])

from lib import *
from move import *
			
def nop_f(state, _, _):
	return [const, state]
		
def traverse_farm(state, f, box=None, start=None):
	state, d = wh(state)
		
	if box == None:
		box = [0, 0, d-1, d-1]
	
	if start == None:
		start = box[:2]

	state = move_to(state, start)

	res = {}
	for yi in range(box[3]):
		y = (start[1] + yi) % d
		for xi in range(box[2]):
			x = (start[0] + xi) % d
	
			state = move_to(state, [x, y])
			xss = f(state, x, y)
			state, out = dos(state, xss)
			res[(x, y)] = out
	return state, res
	
def boxloop(state, box, f, start=None, loop=True):
	def g(state, x, y):
		return [f]
	return farmloop(state, g, loop, False, box, start)

def farmloop(state, f, loop=True, scan=False, box=None, start=None):
	if scan:
		state, out = traverse_farm(state, nop3, box, start)
		
	def go(state):
		return traverse_farm(state, f, box, start)
		
	while True:
		state, out = go(state)
		state["i"] += 1
		if not loop:
			return state, out

from lib import *
from move import *
			
def nop_f(state, _, _):
	return [const, state]
		
def traverse_farm(state, f, box=None):
	if box == None:
		box = [0, 0, wh(state)-1, wh(state)-1]
		
	if state == None:
		state = mk_state()
		
	state = move_to(state, box[:2])
	
	for y in range(box[1], box[1] + box[3]):
		for x in range(box[0], box[0] + box[2]):
			state = move_to(state, [x, y])
			state["here"] = state["grid"][y][x]
			xss = f(state, x, y)
			state = dos(state, xss)
	return state
	
def boxloop(state, box, f):
	def g(state, x, y):
		return [f]
	return farmloop(state, g, True, False, box)

def farmloop(state, f, loop=True, scan=False, box=None):
	if scan:
		state = traverse_farm(state, nop3, box)
		
	def go(state):
		return traverse_farm(state, f, box)
		
	if loop:
		while True:
			state = go(state)
			state["i"] += 1
	else:
		return go(state)

		

		
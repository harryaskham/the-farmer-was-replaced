from lib import *
			
def nop_f(state, _, _):
	return [const, state]
		
def traverse_farm(state, f):
	go_origin()
	if state == None:
		state = mk_state()
	for y in range(wh(state)):
		for x in range(wh(state)):
			state["y"] = y
			state["x"] = x
			state["here"] = state["grid"][y][x]
			xss = f(state, x, y)
			state = dos(state, xss)
			move(East)
		move(North)
	return state

def farmloop(state, f, loop=True, scan=False):
	if scan:
		state = traverse_farm(state, nop3)
		
	def go(state):
		return traverse_farm(state, f)
		
	if loop:
		while True:
			state = go(state)
			state["i"] += 1
	else:
		return go(state)

		

		
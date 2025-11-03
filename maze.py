from lib import *
from planting import *
from harvest import *
from sense import *
from move import *

def maze(state, size=None):
	start_pos = xy(state)
	state = sense(state, False)
	if et(state) not in [E.Hedge, E.Treasure]:
		if size == None:
			size = wh(state)
		use_n = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		state = dos(state, [
			[plant_one, E.Bush],
			[useM, I.Weird_Substance, use_n],
		])
	seen = set()
	back = []
	while True:
		state = sense(state, False)
		
		if et(state) == E.Treasure:
			state = try_harvest(state, [E.Treasure])
			break

		[x, y] = xy(state)
		seen.add((x, y))
		ns = neighbors_dict(state)
		moved = False
		for d in ns:
			n = ns[d]
			if n in seen:
				continue
			state = moveM(state, d)
			if xy(state) != [x, y]:
				moved = True
				back.append(opposite(d))
				break
		if not moved:
			if back == []:
				break
			state = moveM(state, back.pop())
			
	state = move_to(state, start_pos)
	return state
			
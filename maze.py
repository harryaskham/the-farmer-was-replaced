from lib import *
from planting import *
from harvest import *
from sense import *
from move import *
from drones import *

def maze_many(state, size=None):
	state = move_to(state, [wh(state)-1, wh(state)-1])
	state = spawnM(state, [maze, size], 12)
	
	state = move_to(state, [0, wh(state)-1])
	state = spawnM(state, [maze, size], 8)
	
	state = move_to(state, [wh(state)-1, 0])
	state = spawnM(state, [maze, size], 4)
	
	state = move_to(state, [0, 0])
	return maze(state, size)

def maze(state, size=None):
	start_pos = xy(state)
	state = sense(state)
	if et(state) not in [E.Hedge, E.Treasure]:
		if size == None:
			size = wh(state)
		use_n = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
		state = do_(state, [
			[plant_one, E.Bush],
			[useM, I.Weird_Substance, use_n],
		])

	seen = set()
	back = []
	while True:
		state = sense(state)
		
		if et(state) == E.Treasure:
			state = try_harvest(state, [E.Treasure])
			break

		[x, y] = xy(state)
		seen.add((x, y))
		ns = neighbors_dict(state)
		moved = False
		
		ds = []
		if state["treasure"][0] < x:
			ds.append(West)
		if state["treasure"][0] > x:
			ds.append(East)
		if state["treasure"][1] < y:
			ds.append(South)
		if state["treasure"][1] > y:
			ds.append(North)
		for d in [North, East, South, West]:
			ds.append(d)
			
		for d in ds:
			if d not in ns:
				continue
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
			state, _ = moveM(state, back.pop())
			
	state = move_to(state, start_pos)
	return state

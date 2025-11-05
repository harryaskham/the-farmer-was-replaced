from lib import *
from loops import *
from maze import *
from drones import *
from sunflower import *
from pumpkin import *

def filler_maze(state, num_drones=16):
	d = wh(state)
	n = d // (num_drones ** 0.5)
	ps = []
	for x in range(10):
		ps.append([dos, [
			[move_to, [x, d-1]],
			[Sunflower, 7, 7, False, True]
		]])
	for x in range(0, 6 * (d // 6), 6):
		ps.append([boxloop, [x, d-2, 6, 1], [boost_solo]])
	for y in range(n//2, n//2 + n * (d // n), n):
		for x in range(n//2, n//2 + n * (d // n), n):
			ps.append([dos, [
				[move_to, [x, y]],
				[wait_secsM, 5],
				[boxloop, [x, y, 1, 1], [maze, n]]
			]])
	return ps
	
def filler_pumpkin(state):
	d = wh(state)
	state = move_to(state, [d//2, d//2])

	def child(state, c=None):
		if c == None:
			c = xy(state)

		[x, y] = c
		x = x % d
		y = y % d
		return must_spawn(state, [dos, [
			[move_to, [x, y]],
			[sense, False],
			[whileM, [eqM, [etM], [pure, E.Pumpkin]], [dos, [
				[moveM, dir],
				[sense, False]
			]]],
			[water_to, 0.75, 1.0],
			[plant_pumpkin, False],
			[child, [x,y+1], East],
			[child, [x,y+1], West],
		]])
		
	return mapM(state, [child, None], Dirs)
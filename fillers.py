from lib import *
from loops import *
from maze import *
from drones import *
from sunflower import *
from pumpkin import *
from cactus import *
from filler_utils import *
from filler_cactus import *

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

	def child(state, c, dir):
		[x, y] = c
		x = x % d
		y = y % d
		return spawnM(state, [dos, [
			[move_to, [x, y]],
			[child, [(x+3)%d,(y+3)%d], East],
			[sense],
			[whileM, [eqM, [etM], [pure, E.Pumpkin]], [dos, [
				[moveM, dir],
				[water_to, 0.75, 1.0],
				[sense]
			]]],
	
			[plant_pumpkin, False]
		]])
		
	return mapM(state, [child, xy(state)], Dirs)

def filler_crops(state):
	return fill_rows(state, [dos, [
		[sense],
		[try_harvest],
		[Checker3, [plant_one, E.Tree], [plant_one, E.Carrot], [plant_one, E.Grass]],
	]])


def filler_crop(state, e):
	return fill_rows(state, [dos, [
		[sense],
		[try_harvest],
		[plant_one, e]
	]])
	
def filler_energy(state):
	d = wh(state)
	
	def sunflower_at(state, c):
		return spawnM(state, [dos, [
			[move_to, c],
			[Sunflower, 7, 7, True, True, True]
		]])
		
	def boost_at(state, c):
		return spawnM(state, [dos, [
			[move_to, c],
			[forever, [boost, 10, True, True, 15, 15, True, True]]
		]])

	def spaced(n=32, gap=1):
		cs = []
		for y in range(0, d, gap+1):
			for x in range(0, d, gap+1):
				cs.append([x, y])
				if len(cs) == n:
					break
			if len(cs) == n:
				break
		return cs
		
	def sunflower_row(n=10):
		cs = []
		for x in range(n):
			cs.append([x, d-1])
		return cs
		
	def planter(state, y):
		return dos(state, [
			[boxloop, [0, y, d, 1], [dos, [
				[Sunflower, 7, 15]
			]]]
		])

	def harvester(state, y):
		state["petal_threshold"] = 15
		
		def decr(state):
			state["petal_threshold"] -= 1
			return state
			
		def reset(state):
			state["petal_threshold"] = 15
			return state
			
		def do_harv(state):
			state, h = get_here(state)
			petals = h["petals"]
			return pure(state, petals != None and petals >= state["petal_threshold"])

		return dos(state, [
			[boxloop, [0, y, d, 1], [dos, [
				[sense],
				[whenM, [do_harv], [dos, [
					[try_harvest],
					[reset]
				]]],
				[whenM, [bind, [xy], [eq, [d-1, y]]], [decr]]
			]]]
		])
		
	return dos(state, [
		[mapM, [sunflower_at], sunflower_row()],
		[wait_all],
		[mapM, [boost_at], spaced()[1:]],
		[forever, [boost]]
	])


def filler_companions(state):
	return fill_rows(state, [dos, [
		[sense],
		[try_harvest, None, False, False, [Companions.AWAIT]],
		[Companion, [Checker3, [plant_one, E.Tree], [plant_one, E.Carrot], [plant_one, E.Grass]]],
		[sense],
		[return_row]
	]], merge_rows)

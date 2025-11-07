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

	def child(state, c, dir):
		[x, y] = c
		x = x % d
		y = y % d
		return spawnM(state, [dos, [
			[move_to, [x, y]],
			[child, [(x+3)%d,(y+3)%d], East],
			[sense, False],
			[whileM, [eqM, [etM], [pure, E.Pumpkin]], [dos, [
				[moveM, dir],
				[water_to, 0.75, 1.0],
				[sense, False]
			]]],
	
			[plant_pumpkin, False]
		]])
		
	return mapM(state, [child, xy(state)], Dirs)

def filler_crops(state):
	d = wh(state)
	
	def spaced(n=32, gap=5):
		cs = []
		for y in range(0, d, gap+1):
			for x in range(0, d, gap+1):
				cs.append([x, y])
				if len(cs) == n:
					break
			if len(cs) == n:
				break
		return cs

	def p(c):
		
		return [boxloop, [0, 0, d, d], [dos, [
			[sense, False],
			[try_harvest],
			[water_to],
			[runSXY, [Checker, [plant_one, E.Tree], [plant_one, E.Carrot]]],
			[sense, True]
		]], c, True]
		
	for y in range(1, 32):
		state = spawnM(state, p([0, y]))
	return dos(state, [p([0, 0])])
	
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
			petals = get_here(state)["petals"]
			return pure(state, petals != None and petals >= state["petal_threshold"])

		return dos(state, [
			[boxloop, [0, y, d, 1], [dos, [
				[sense, False],
				[whenM, [do_harv], [dos, [
					[try_harvest],
					[reset]
				]]],
				[whenM, [bind, [xy], [eq, [d-1, y]]], [decr]]
			]]]
		])
		
	#for y in range(1, 16):
	#	state = spawnM(state, [planter, y])
	#	state = spawnM(state, [harvester, y])
		
	#state = spawnM(state, [planter, 0])
	#state = harvester(state, 0)
	
	#return state

	return dos(state, [
		[mapM, [sunflower_at], sunflower_row()],
		[wait_all],
		[mapM, [boost_at], spaced()[1:]],
		[forever, [boost]]
	])

	
	
def fill_rows(state, f):
	d = wh(state)
	def p(y):
		return [boxloop, [0, y, d, 1], f, [0, y], False]
	for y in range(1, d):
		state = spawnM(state, p(y))
	state = do_(state, [p(0)])
	state, y_rows = wait_all(state)
	for y, row in y_rows:
		state["grid"][y] = row
	return State.inc_loop_index(state)

def filler_companions(state):
	def select_loop(state):
		return pure(state, state["i"] % 2 == 0)
		
	def return_row(state):
		return pure(state, (state["y"], state["grid"][state["y"]]))
		
	return fill_rows(state, [dos, [
		[sense, True],
		[condM, [select_loop],
			[dos, [
				[Checker3,
					[plant_one, E.Tree],
					[plant_one, E.Carrot],
					[plant_one, E.Grass]
				]
			]],
			[dos, [
				[Companion]
			]]
		],
		[return_row]
	]])
	

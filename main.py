from farmlib import *

def cleanupXY(state, x, y):
	return cleanup(state)
			
def runSXY(state, f):
	f = list(f)
	f.insert(1, state["y"])
	f.insert(1, state["x"])
	return dos(state, [f])
	
def runSXY2(state, f, g=[]):
	f = list(f)
	f.insert(1, state["y"])
	f.insert(1, state["x"])
	for x in g:
		f.append(x)
	return dos(state, [f])

def wrapXY(f):
	def g(state, x, y):
		return f(state)
	return g

def nop1(state):
	return state
	
def progs(state):
	n = wh(state)
	return [
		[boxloop, [0, 0, n, 8], [dos, [
			[runSXY, [Box, [10, 0, 8, 7], [nop1], [runSXY, [Checker, [plant_one, E.Tree], [plant_one, E.Carrot]]]]]
		]]],
		[boxloop, [0, 0, n, 8], [dos, [
			[runSXY, [Box, [10, 0, 8, 7], [dos, [
				[runSXY, [Box, [0, 0, 10, 1], [Sunflower, 7, 7], [runSXY, [Cactus, [10, 0, 8, 8], [nop1]]]]]
			]]]]
		]]],
		[boxloop, [0, n-6, 6*3,6], [dos, [
			chain([
				[runSXY2, [Pumpkin, [0, n - 6, 6, 6]]],
				[runSXY2, [Pumpkin, [6, n - 6, 6, 6]]],
				[runSXY2, [Pumpkin, [12, n - 6, 6, 6]]],
				[nop1]
			])
		]]]
	]

def run_progs(state):
	ps = progs(state)
	for p in ps[:-2]:
		state = spawnM(state, p)
	return dos(state, [p[-1]])
	




def loop(state, x, y):
	return [
		[debug, ""],
		[when, x == 0 and y == 8, [dos, [
			[spawnM, [main]]
		]]],
		[sense, False],
		[bind, [here], [debug]],
		[cleanup],
		[try_harvest, ALWAYS_HARVEST],
		[Box, x, y, [0, 0, 10, 1],
			[Sunflower, 7, 7],
			[dos, [
				[when, x == 0, [boost, BOOSTS]],
				chain([
					[Pumpkin, x, y, [0, wh(state) - 6, 6, 6]],
					[Pumpkin, x, y, [6, wh(state) - 6, 6, 6]],
					[Pumpkin, x, y, [12, wh(state) - 6, 6, 6]],
					[Cactus, x, y, [10, 0, 8, 8]],
					[Companion],
					[Box, x, y, [0, 1, 10, 11], [plant_one, E.Carrot]],
					[Checker, x, y, [plant_one, E.Tree]],
					[plant_one, E.Grass]
				]),
				[fertilize_loop, FERTILIZE["entities"], FERTILIZE["repeats"]]
			]]
		],
		[sense, True],
		[bind, [here], [debug]],
	]
	
def harvest_loop(state, x, y):
	return [
		[sense, False],
		[cleanup],
		[when, x == 0 and y > 0, [boost, BOOSTS]],
		[try_harvest, ALWAYS_HARVEST],
		[sense, True],
	]

def do_purge_all(state, x, y):
	return [
		[try_harvest],
		[maybe_untill]
	]
	
def do_purge(state, x, y):
	return [
		[sense, False],
		[try_harvest, [E.Pumpkin, E.Dead_Pumpkin, E.Tree, E.Carrot, E.Cactus, E.Bush]],
		[sense, True]
	]
	
def do_scan(state, x, y):
	return [
		[sense, True]
	]
	
def do_dino(state, x, y):
	return [
		[dino, dumb]
	]

def do_maze(state, x, y):
	return [
		[maze_many]
	]

def main(state):	
	dos(state, [
		[hatM, Hats.Wizard_Hat],
		[when, PURGE, [dos, [
			[farmloop, do_purge, False]
		]]],
		[when, PURGE_ALL, [dos, [
			[farmloop, do_purge_all, False]
		]]],
		[when, PROGS, [dos, [
			[run_progs]
		]]],
		[when, MAZE, [dos, [
			[try_harvest, [E.Treasure, E.Hedge]],
			[farmloop, do_maze]
		]]],
		[when, DINO, [dos, [
			[farmloop, do_dino]
		]]],
		[when, SCAN, [dos, [
			[farmloop, do_scan, False]
		]]],
		[when, FARM, [dos, [
			[bind, [cache_loop, loop], [farmloop]]
		]]]
	])

state = mk_state()
main(state)
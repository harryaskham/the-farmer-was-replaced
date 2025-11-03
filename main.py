from farmlib import *
			
def loop(state, x, y):
	return [
		[debug, ""],
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
					[Cactus, x, y, [10, 0, 12, 12]],
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
		[maze]
	]
	
state = mk_state()

dos(state, [
	[hatM, Hats.Wizard_Hat],
	[when, PURGE, [dos, [
		[farmloop, do_purge, False]
	]]],
	[when, PURGE_ALL, [dos, [
		[farmloop, do_purge_all, False]
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

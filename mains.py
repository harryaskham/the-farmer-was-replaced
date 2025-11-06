from farmlib import *

def loop(state, x, y):
	return [
		[debug, ""],
		[when, x == 0 and y == 8, [dos, [
			[spawnM, [farmloop, loop]]
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

def do_purge_all(state, x, y):
	return [
		[try_harvest],
		[maybe_untill]
	]
	
def do_purge(state, x, y):
	return [
		[sense, False],
		[try_harvest, [E.Pumpkin, E.Dead_Pumpkin, E.Tree, E.Carrot, E.Cactus, E.Bush]]
	]
	
def do_scan(state, x, y):
	return [
		[sense, True]
	]
	
def do_dino(state, x, y):
	return [
		[dino, search_apple]
	]

def do_maze(state, x, y):
	return [
		[maze_many]
	]
	
	
def do_flips(state):
	return dos(state, [
		[forM, range(32),
			[constM,
				[spawn,
					[dos, [
						[bind, [ixy], [move_to]],
						[forever, [do_a_flipM]]
					]],
					[Spawn.BECOME]
				]
			]
		]
	])
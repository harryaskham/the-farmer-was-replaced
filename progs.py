from farmlib import *


def purges(state, n_drones=None):
	n = wh(state)
	if n_drones == None:
		n_drones = state["max_drones"]
	every = n // n_drones
	ps = []
	for y in range(0, n-every, every):
		ps.append([boxloop, [0, y, n, every], [try_harvest]])
	return ps

def progs(state):
	n = wh(state)
	return [
		[boxloop, [0, 0, 10, 10], [dos, [
			[hatM, Hats.Brown_Hat],
			[sense, False],
			[try_harvest],
			[runSXY, [Checker, [plant_one, E.Tree], [plant_one, E.Carrot]]],
			[sense, True]
		]]],
		[boxloop, [12, 0, 10, 10], [dos, [
			[hatM, Hats.Green_Hat],
			[sense, False],
			[runSXY,
				[Box, [12, 0, 10, 1],
					[Sunflower, 7, 7, True, True],
					[runSXY, [Cactus, [12, 1, 10, 9], [nop1]]]
				]
			],
			[sense, True]
		]]],
		[boxloop, [0, n-6, 7*3, 6], [dos, [
			[hatM, Hats.Gold_Hat],
			[sense, False],
			[cleanup],
			chain([
				[runSXY1, [Pumpkin, [0, n - 6, 6, 6]]],
				[runSXY1, [Pumpkin, [7, n - 6, 6, 6]]],
				[runSXY, [Pumpkin, [14, n - 6, 6, 6], [nop1]]]
			]),
			[sense, True]
		]]],
		[boxloop, [18, 10, 4, 6], [dos, [
			[hatM, Hats.Straw_Hat],
			[try_harvest]
		]]],
		[boxloop, [10, 0, 1, 1], [dos, [
			[hatM, Hats.Sunflower_Hat],
			[boost, 1, False, True]
		]]],
		[boxloop, [11, 0, 1, 1], [dos, [
			[hatM, Hats.Sunflower_Hat],
			[boost, 1, False, True]
		]]],
		[boxloop, [3, 13, 1, 1], [dos, [
			[hatM, Hats.Sunflower_Hat],
			[maze, 6]
		]]],
		[boxloop, [9, 13, 1, 1], [dos, [
			[hatM, Hats.Sunflower_Hat],
			[maze, 6]
		]]],
		[boxloop, [15, 13, 1, 1], [dos, [
			[hatM, Hats.Sunflower_Hat],
			[maze, 6]
		]]]
	]

def run_progs(state, mk_fs):
	ps = mk_fs(state)
	for p in ps[:-1]:
		state = spawnM(state, p)
	return dos(state, [ps[-1]])
from farmlib import *
from mains import *
from progs import *
	
def main(state):	
	dos(state, [
		[hatM, Hats.Straw_Hat],
		[move_to, [0, 0]],
		[try_harvest],
		[when, PURGE, [dos, [
			[run_progs, purges]
		]]],
		[when, PROGS, [dos, [
			[run_progs, progs]
		]]],
		[when, PUMPKIN and FILL, [dos, [
			[filler_pumpkin]
		]]],
		[when, ENERGY and FILL, [dos, [
			[filler_energy]
		]]],
		[when, MAZE, [dos, [
			[cond, FILL,
				[run_progs, filler_maze],
				[dos, [
					[try_harvest, [E.Treasure, E.Hedge]],
					[farmloop, do_maze]
				]]
			]
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
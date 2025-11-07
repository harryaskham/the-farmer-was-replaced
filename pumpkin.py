from lib import *
from harvest import *
from pattern import *
from planting import *
from sense import *	

def pumpkin_died(state):
	def done():
		return can_harvest() or get_entity_type() == E.Dead_Pumpkin
	while not done():
		pass
	return dos(state, [
		[sense],
		[pure, not can_harvest()]
	])
		
def plant_pumpkin(state, do_fertilize=True):
	state, e = et(state)
	if e == E.Pumpkin:
		return state
	return dos(state, [
		[try_harvest, [E.Dead_Pumpkin]],
		[cond, do_fertilize,
			[plantM, E.Pumpkin],
			[plant_one, E.Pumpkin]],
		[whenM, [pumpkin_died], [plant_pumpkin, do_fertilize]]
	])

def Pumpkin(state, x, y, box, otherwise, do_fertilize=True, do_harvest=True):
	return dos(state, [
		[Box, x, y, box,
			[dos, [
				[when, state["id"] == 0 and [x, y] == corner(box, SW), [dos, [
					[when, do_harvest, [dos, [
						[try_harvest, [E.Pumpkin]],
						[set_box_harvested, box]
					]]]
				]]],
				[plant_pumpkin, do_fertilize]
			]],
			otherwise
		]
	])

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
		[pushret, not can_harvest()]
	])
		
def maybe_replant(state):
	return dos(state, [
		[try_harvest, [E.Dead_Pumpkin]],
		[plantM, E.Pumpkin],
		[whenM, [pumpkin_died], [maybe_replant]]
	])

def Pumpkin(state, x, y, box, otherwise):
	return dos(state, [
		[Box, x, y, box,
			[dos, [
				[when, [x, y] == corner(box, NE), [dos, [
					[try_harvest, [E.Pumpkin]]
				]]],
				[maybe_replant]
			]],
			otherwise
		]
	])
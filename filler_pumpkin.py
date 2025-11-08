from lib import *
from drones import *
from pumpkin import *
from filler_utils import *

def filler_pumpkin(state):
	def reviver(c):
		def go(state):
			return dos(state, [
				[move_to, c],
				[cleanup],
				[plant_pumpkin]
			])

	def handler(state, results):
		state, d = wh(state)
		done = True
		for result in values(results):
			for c in result:
				planted, dead = result[c]
				#info(state, (planted, dead))
				#if dead:
				#	state = spawn(state, [reviver], [Spawn.AWAIT])
				if planted:
					done = False
		if done:
			return dos(state, [
				[try_harvest],
				[set_box_harvested, [0, 0, d, d]]
			])
		return state
		
	return fill_rows(state, [dos, [
		[sense],
		[liftA2, [pair],
			[plant_one, E.Pumpkin],
			[pure, False]
			#[dos, [	
			#	[sense],
			#	[bind, [et], [eq, E.Dead_Pumpkin]]
			#]]
		]
	]], handler)
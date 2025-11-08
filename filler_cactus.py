from lib import *
from drones import *
from cactus import *
from filler_utils import *


def filler_cactus(state):
	def handler(state, results):
		state, d = wh(state)
		all_done = True
		
		#info(state, ("results", results))
		for result in values(results):
		
			#info(state, ("result", result))
			for x, y in result:
				one_result = result[(x, y)]
				((planted, sorted), row) = one_result
				if x == d - 1:
					state["grid"][y] = row
				if planted or sorted:
					all_done = False
				
		if not all_done:
			return state
			
		return dos(state, [
			[try_harvest]
		])
			
	return fill_rows(state, [dos, [
		[sense, [Sensing.DIRECTIONAL]],
		[wait_secsM, state["id"] / 32.0],
		[liftA2, [pair],
			[liftA2, [pair],
				[plant_one, E.Cactus],
				[emplace_cactus, [West]]
			],
			[get_row]
		]
	]], handler)
from lib import *
from drones import *
from cactus import *
from filler_utils import *

def filler_cactus(state):
	def handler(state, results):
		moved = result_list(state, results)
		if any(moved):
			return state
		return dos(state, [
			[try_harvest]
		])
			
	return fill_rows(state, [dos, [
		[plant_one, E.Cactus],
		[sort_cactus, [East, West]],
	]], handler)
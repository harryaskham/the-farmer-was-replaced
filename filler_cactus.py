from lib import *
from drones import *
from cactus import *
from filler_utils import *

def filler_cactus(state):
	def handler(state, results):
		state, rs = result_list(state, results)
		state = info(state, ("rs", rs))
		state, _ = clearret(state)
		if all(rs):
			return dos(state, [
				[try_harvest]
			])
		return state
			
	return fill_rows(state, [dos, [
		[sense],
		[bind, [plant_one, E.Cactus], [pushret]],
		[bind, [emplace_cactus], [pushret]],
		[liftA2, [pair],
			[bind, [State.get, "ret"], [noneM]],
			[return_row]
		]
	]], handler, 5)
from lib import *
from debug import *
from measure import *

def sense(state, set_companion=False):
	e = get_entity_type()
	state = dos(state, [
		[set_here, {
			"entity_type": e,
			"ground_type": get_ground_type()
		}],
		[when, e == E.Cactus, [measureM, "cactus_size"]],
		[when, e == E.Sunflower, [measureM, "petals"]],
		[when, e == E.Apple, [set_state, {"apple": measure()}]]
	])

	companion = get_companion()
	if companion == None:
		return debug(state, "no companion", 5)
		
	state = dos(state, [
		[debug, "companion", 5],
		[debug, companion, 5],
		[debug, "target", 5],
		[bind, [at, companion[1]], [flipM, debug, 5]]
	])
		
	if not set_companion:
		return state
		
	return dos(state, [
		[set_at, companion[1], {
			"companion": companion[0],
		}],
		[set_here, {
			"companion_at": companion[1]
		}],
	])
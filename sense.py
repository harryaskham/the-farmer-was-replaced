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
		[when, e == E.Apple, [set_state, {"apple": measure()}]],
		[when, e == E.Hedge, [set_state, {"treasure": measure()}, [To.CHILDREN]]]
	])
		
	if not set_companion:
		return state
		
	companion = get_companion()
	if companion == None:
		return verbose(state, "no companion")
		
	state = dos(state, [
		[debug, "companion/target"],
		[debug, companion],
		[bind, [at, companion[1]], [debug]]
	])

		
	return dos(state, [
		[set_at, companion[1], {"companion": companion[0]}, [To.CHILDREN]],
		[set_here, {"companion_at": companion[1]}, [To.CHILDREN]]
	])
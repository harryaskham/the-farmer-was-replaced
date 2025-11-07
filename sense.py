from lib import *
from debug import *
from measure import *
import State

def sense(state, set_companion=True):
	e = get_entity_type()
	g = get_ground_type()
	state = do_(state, [
		[set_here, {
			"entity_type": e,
			"ground_type": g
		}],
		[when, e == E.Cactus, [measureM, "cactus_size"]],
		[when, e == E.Sunflower, [measureM, "petals"]],
		[when, e == E.Apple, [State.set, {"apple": measure()}]],
		[when, e == E.Hedge, [State.set, {"treasure": measure()}, [To.CHILDREN]]]
	])
		
	if not set_companion:
		return state
		
	companion = get_companion()
	if companion == None:
		return verbose(state, "no companion")

	return do_(state, [
		[cond, companion == None,
		 [verbose, "no companion"],
		 [dos, [
			[debug, "companion/target"],
			[debug, companion],
			[bind, [at, companion[1]], [debug]],
			[set_at, companion[1], {"companion": companion[0]}, [To.CHILDREN]],
			[set_here, {"companion_at": companion[1]}, [To.CHILDREN]]
		 ]]
		]
	])

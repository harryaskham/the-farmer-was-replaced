from lib import *
from items import *
from planting import *
from fertilizer import *

def harvestM(state):
	harvest()
	c_at = get_here(state, "companion_at")
	return dos(state, [
		[set_here, {
			"entity_type": None,
			"infected": False,
			"petals": None,
			"cactus_size": None,
			"companion": None,
			"companion_at": None
		}],
		[when, c_at != None, [set_at, c_at, {
			"companion": None
		}]]
	])


def try_harvest(state, entities=None):
	if entities == None or contains(entities, et(state)):
		if get_here(state, "companion") != None and not HARVEST_COMPANIONS:
			return state
		if can_harvest():
			return dos(state, [
				[maybe_cure],
				[harvestM]
			])
	return state
		
def set_box_harvested(state, box):
	[x0, y0, w, h] = box
	for y in range(y0, y0 + h):
		for x in range(x0, x0 + w):
			state = set_at(state, [x, y], {
				"entity_type": None
			})
	return state		
		
def cleanup(state):
	return try_harvest(state, [E.Dead_Pumpkin])

def fertilize_loop(state, over=None, n=None):
	e = et(state)
	if (over == None or contains(over, e)) and (n == None or n > 0):
		i = 0
		while num_items(I.Fertilizer) > 0 and (n == None or i < n):
			state = dos(state, [
				[fertilize, [e]],
				[try_harvest, [e]],
				[plantM, e]
			])
			i += 1
	return state
	
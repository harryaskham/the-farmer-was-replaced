from lib import *
from items import *
from planting import *
from fertilizer import *
from move import *

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
		}, [To.CHILDREN]],
		[when, c_at != None, [set_at, c_at, {
			"companion": None
		}, [To.CHILDREN]]]
	])


def try_harvest(state, entities=None, cure=True, unsafe=False, flags=[]):
	flags = set(flags)
	if not (entities == None or contains(entities, et(state))):
		return state
		
	c_at = get_here(state, "companion_at")
	if c_at != None:
		cn = at(state, c_at)
		companion = cn["companion"]
		planted = cn["entity_type"]
		if (
			Companions.PLANT in flags
			and c_at != None
			and companion != None
			and planted != companion
		):
			here = xy(state)
			state = dos(state, [
				[move_to, c_at],
				[plant_one, companion],
				[sense, True],
				[move_to, here],
			])
			
	is_companion = (
		et(state) != None
		and get_here(state, "companion") == et(state))
	
	if Companions.AWAIT in flags:
		while True:
			cn = at(state, get_here(state, "companion_at"))
			if cn["companion"] == None or cn["entity_type"] == cn["companion"]:
				break
	elif Companions.RESERVE in flags and is_companion:
		return state
			
	if can_harvest():
		return dos(state, [
			[when, cure, [maybe_cure, entities, unsafe]],
			[harvestM]
		])

	return state
	
def wait_for_harvest(state, delay=0.5):
	while not can_harvest():
		wait_secs(delay)
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
	
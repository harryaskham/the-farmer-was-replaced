from lib import *
from fertilizer import *
from water import *
from flags import *
from sense import *

def tillable(e):
	return contains([
		None,
		E.Carrot,
		E.Pumpkin,
		E.Sunflower,
		E.Cactus
	], e)
	
def untillable(e):
	return contains([
		None,
		E.Grass
	], e)
	
def plantable(e):
	return e != Entities.Grass

def maybe_till(state, e):
	if tillable(e) and gt(state)[1] != G.Soil:
		till()
		return set_here(state, {
			"ground_type": G.Soil
		})
	return state

def maybe_untill(state, e=None):
	if untillable(e) and gt(state)[1] != G.Grassland:
		till()
		return set_here(state, {
			"ground_type": G.Grassland
		})
	return state
		
def maybe_plant(state, e, water=False):
	if plantable(e) and et(state)[1] != e:
		if water:
			state = water_to(state, WATER_RANGE[0], WATER_RANGE[1], WATER_BEFORE)
		plant(e)
		return dos(state, [
			[set_here, {"entity_type": e}],
			[sense],
			[pure, True]
		])
	return pure(state, False)

def plant_one(state, e, unused=None):
	return dos(state, [
		[maybe_till, e],
		[maybe_untill, e],
		[maybe_plant, e, True]
	])
	
def plantM(state, e, unused=None):
	state, planted = plant_one(state, e)
	return dos(state, [
		[fertilize],
		[maybe_cure],
		[pure, planted]
	])

		
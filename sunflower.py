from lib import *
from harvest import *
from measure import *

def Sunflower(state, min_petals=7, max_petals=15, force=False, fertilize=False):
	if not force and et() == E.Sunflower and measure() >= min_petals and measure() <= max_petals:
		return state
		
	while state["here"]["petals"] == None or state["here"]["petals"] < min_petals or state["here"]["petals"] > max_petals:
		state = dos(state, [
			[try_harvest],
			[when, fertilize, [plantM, E.Sunflower]],
			[when, not fertilize, [plant_one, E.Sunflower]],
			[measureM, "petals"]
		])
	return state
		
def boost(state, n=10, fertilize=True, water=True):
	state = try_harvest(state)
	if water:
		state = water_to(state, 0.75, 1.0)
	for _ in range(n):
		state = dos(state, [
			[Sunflower, 7, 15, True, fertilize],
			[when, not fertilize, [wait_secsM, 3]],
			[try_harvest]
		]) 
	return state
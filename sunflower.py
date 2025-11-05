from lib import *
from harvest import *
from measure import *

def Sunflower(state, min_petals=7, max_petals=15, force=False, do_fertilize=False):
	if not force and et() == E.Sunflower and measure() >= min_petals and measure() <= max_petals:
		return state
		
	while True:
		state = dos(state, [
			[harvestM],
			[plant_one, E.Sunflower],
			[measureM, "petals"]
		])
		[x, y] = xy(state)
		petals = here(state)["petals"]
		if petals >= min_petals and petals <= max_petals:
			break

	return when(state, do_fertilize, [fertilize])
		
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
	
def boost_box(state, box, num_flowers=10, boosts=10, force=False, fertilize=True, water=True):
	[x0, y0, w, h] = box
	i = 0
	flowers = set()
	for y in range(y0, y0 + h):
		for x in range(x0, x0 + w):
			flowers.add((x, y))
			i += 1
			if i == num_flowers:
				break
		if i == num_flowers:
			break
	[hx, hy] = xy(state)
	if (hx, hy) in flowers:
		return Sunflower(state, 7, 7, force, fertilize)
	else:
		return boost(state, boosts, fertilize, water)
		
def boost_solo(state):
	return dos(state, [
		[try_harvest],
		[water_to, 0.75, 1.0],
		[Sunflower]
	])
	
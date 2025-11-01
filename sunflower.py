from lib import *
from harvest import *
from measure import *

def Sunflower(state, min_petals=7, max_petals=15, force=False):
	if not force and et() == E.Sunflower and measure() >= min_petals and measure() <= max_petals:
		return state
		
	while state["here"]["petals"] == None or state["here"]["petals"] < min_petals or state["here"]["petals"] > max_petals:
		state = dos(state, [
			[try_harvest],
			[plantM, E.Sunflower],
			[measureM, "petals"]
		])
	return state
		
def boost(state, n=10):
	if et(state) == E.Sunflower:
			return state
			
	for _ in range(n):
		state = dos(state, [
			[Sunflower],
			[try_harvest]
		]) 
	return state
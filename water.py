from lib import *
from items import *
from flags import *

def water_to(state, min=WATER_RANGE[0], max=WATER_RANGE[1], over=None):
	state, e = et(state)
	if over == None or contains(over, e):
		if max == None:
			max = min
		if get_water() < min:
			while get_water() < max:
				state = useM(state, I.Water)
	return state

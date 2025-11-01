from lib import *
from items import *

def water_to(state, min=0, max=None, over=None):
	if over == None or contains(over, et(state)):
		if max == None:
			max = min
		if get_water() < min:
			while get_water() < max:
				state = useM(state, I.Water)
	return state

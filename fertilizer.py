from lib import *
from items import *

def fertilizable(e):
	return not contains([
		E.Dead_Pumpkin,
		None
	], e)

def fertilize(state, over=None, n=None):
	if over == None or contains(over, et(state)):
		i = 0
		while fertilizable(et(state)) and not can_harvest() and (n == None or i < n) and num_items(I.Fertilizer) > 0:
			state = dos(state, [
				[useM, I.Fertilizer]
			])
			i += 1
	return state

def maybe_cure(state, over=None):
	if over == None or contains(over, et(state)):
		if get_here(state, "infected"):
			return dos(state, [
				[useM, I.Weird_Substance],
				[useM, I.Fertilizer],
				[useM, I.Weird_Substance],
			])
	return state

	

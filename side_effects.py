from lib import *
from sense import *
 
def toggle_infected(state, c=None):
	if c == None:
		c = xy()
	return set_at(state, c, {
		"infected": not get_at(state, c, "infected")
	})

SIDE_EFFECTS = {
	I.Fertilizer: [dos, [
		[set_here, { "infected": True }],
		[sense, True]
	]],
	I.Weird_Substance: [dos, [
		[toggle_infected],
		[bind, [neighbors], [mapM, [toggle_infected]]]
	]],
	I.Water: [set_here, { "water": get_water() } ]
}
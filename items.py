from lib import *
from side_effects import *

def useM(state, item):
	use_item(item)
	if item in SIDE_EFFECTS:
		xs = SIDE_EFFECTS[item]
		return dos(state, [xs])
	return state
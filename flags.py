from aliases import *

MAIN_FLAGS = set([
	Mode.SIMULATE,
	Log.DEBUG,
	Size.SMALL,
	Phase.COMPANIONS,
	#Phase.ENERGY,
	#Phase.FLIPS,
	Space.FILL,
])

GLOBAL_DEBUG = True

WATER_RANGE = (0.75, 1.0)
WATER_BEFORE = [
	E.Pumpkin,
	E.Sunflower
]
ALWAYS_HARVEST = [
	E.Grass,
	E.Tree,
	E.Carrot,
	E.Bush
]
HARVEST_FLAGS = [
	Companions.RESERVE
]
FERTILIZE = {
	"entities": ALWAYS_HARVEST,
	"repeats": 0
}
BOOSTS = 3


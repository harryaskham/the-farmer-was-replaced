from lib import *

DEBUG = True
AIR_DEBUG = False
WATER_RANGE = (0.75, 1.0)
WATER_BEFORE = [
	E.Pumpkin,
	E.Sunflower
]
ALWAYS_HARVEST = [
	E.Grass,
	E.Tree,
	E.Carrot,
]
HARVEST_COMPANIONS = True
FERTILIZE = {
	"entities": ALWAYS_HARVEST,
	"repeats": 0
}
BOOSTS = 1

SCAN = False
PURGE = False
FARM = True

from aliases import *

MAIN_FLAGS = set([
    Mode.SIMULATE,
    Mode.TEST,
    Testing.LOOP,
    #Log.DRONE_DETAILS,
    Log.INFO,
    Size.NORMAL,
    Space.FILL,
    #Phase.COMPANIONS,
    #Phase.CROPS,
    #Phase.CARROTS,
    Phase.CACTUS,
    #Phase.PUMPKIN,
    #Phase.ENERGY,
    #Phase.DINO,
    #Phase.FLIPS,

])

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


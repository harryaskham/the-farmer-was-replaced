from aliases import *

MAIN_FLAGS = set([
    #Mode.SIMULATE,
    #Size.SMALL,  
    #Mode.TEST,
    Mode.RUN,
    #Mode.LOOP,
    #Testing.LOOP,
    #Log.DRONE_DETAILS,
    #Log.SHOW_LEVEL,
    Log.INFO,
    Size.TINY,
    Space.FILL,
    #Phase.PURGE,
    #Phase.COMPANIONS,
    #Phase.CROPS,
    #Phase.CARROTS,
    #Phase.CACTUS,
    #Phase.PUMPKIN,
    Phase.MAZE,
    #Phase.ENERGY,
    #Phase.DINO,
    #Phase.FLIPS,
])

ONLY_LOG_DRONES = None
#ONLY_LOG_DRONES = set(["1", "1.7"])

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


from lib import *
from fertilizer import *
from water import *
from flags import *
from sense import *

def tillable(e):
    return contains([
        None,
        E.Carrot,
        E.Pumpkin,
        E.Sunflower,
        E.Cactus
    ], e)

def untillable(e):
    return contains([
        None,
        E.Grass
    ], e)

def plantable(e):
    return e != Entities.Grass

def maybe_till(state, e):
    if tillable(e) and gt(state)[1] != G.Soil:
        till()
        return set_here(state, {
            "ground_type": G.Soil
        })
    return state

def maybe_untill(state, e=None):
    if untillable(e) and gt(state)[1] != G.Grassland:
        till()
        return set_here(state, {
            "ground_type": G.Grassland
        })
    return state

def maybe_plant(state, e, flags=[]):
    flags = set(flags)
    return do(state, [
        [cond, plantable(e) and et(state)[1] != e,
            [do, [
                [when, Growing.WATER in flags, [water_to]],
                [lift([plant]), e],
                [set_here, {"entity_type": e}],
                [sense, flags],
                [pure, True]
            ]],
            [pure, False]
        ]
    ])

def plant_one(state, e, flags=[]):
    return do(state, [
        [maybe_till, e],
        [maybe_untill, e],
        [maybe_plant, e, flags]
    ])

def plantM(state, e, flags=[]):
    flags = set(flags)
    state, planted = plant_one(state, e, flags)
    return do(state, [
        [when, Growing.FERTILIZE in flags, [do, [
            [fertilize, None, 1],
            [when, Growing.AWAIT in flags, [fertilize]]
        ]]],
        [when, Harvesting.CURE in flags, [do, [
            [maybe_cure, [e], Harvesting.UNSAFE in flags],
        ]]],
        [pure, planted]
    ])

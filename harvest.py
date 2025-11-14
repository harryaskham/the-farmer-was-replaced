from lib import *
from items import *
from planting import *
from fertilizer import *
from move import *

def harvestM(state, flags=[]):
    flags = set(flags)
    harvest()
    state, c_at = get_here(state, "companion_at")
    return dos(state, [
        [set_here, {
            "entity_type": None,
            "infected": False,
            "petals": None,
            "cactus_size": None,
            "companion_at": None
        }, flags],
        [when, c_at != None, [set_at, c_at, {
            "companion": None
        }, flags]]
    ])

def gatherM(state, flags=[]):
    return try_harvest(state, None, flags)

def try_harvest(state, entities=None, flags=[]):
    flags = set(flags)
    state, e = et(state)
    if not (entities == None or contains(entities, e)):
        return state

    state, c_at = get_here(state, "companion_at")
    if c_at != None:
        state, cn = at(state, c_at)
        companion = cn["companion"]
        planted = cn["entity_type"]
        if (
            Companions.PLANT in flags
            and c_at != None
            and companion != None
            and planted != companion
        ):
            state, h = xy(state)
            state = do_(state, [
                [move_to, c_at, flags],
                [plant_one, companion, flags],
                [sense, flags],
                [move_to, h],
            ])

    is_companion = e != None and get_here(state, "companion")[1] == e

    if Companions.AWAIT in flags:
        state, c_at = get_here(state, "companion_at")
        state, cn = at(state, c_at)
        if cn != None and (cn["companion"] == None or cn["entity_type"] == cn["companion"]):
            return state

    if Companions.RESERVE in flags and is_companion:
        return state

    if can_harvest():
        return do_(state, [
            [when, Harvesting.CURE in flags, [maybe_cure, entities, Harvesting.UNSAFE in flags]],
            [harvestM]
        ])

    return state

def wait_for_harvest(state, delay=0.5):
    while not can_harvest():
        wait_secs(delay)
    return state

def set_box_harvested(state, box):
    [x0, y0, w, h] = box
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            state = set_at(state, (x, y), {
                "entity_type": None
            })
    return state

def cleanup(state):
    return try_harvest(state, [E.Dead_Pumpkin])

def fertilize_loop(state, over=None, n=None):
    state, e = et(state)
    if (over == None or contains(over, e)) and (n == None or n > 0):
        i = 0
        while num_items(I.Fertilizer) > 0 and (n == None or i < n):
            state = do_(state, [
                [fertilize, [e]],
                [try_harvest, [e]],
                [plantM, e]
            ])
            i += 1
    return state

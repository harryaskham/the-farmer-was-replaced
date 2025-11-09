from dict import *

def mk_cell_state(x, y, kwargs=None):
    if kwargs == None:
        kwargs = {}
    state = {
        "x": x,
        "y": y,
        "entity_type": None,
        "ground_type": None,
        "companion": None,
        "companion_at": None,
        "companion_from": None,
        "infected": False,
        "water": None,
        "petals": None,
        "cactus_size": None
    }
    for k in kwargs:
        state[k] = kwargs[k]
    return state
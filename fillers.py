from farmlib import *
from filler_cactus import *
from filler_companions import *
from filler_energy import *
from filler_pumpkin import *
from filler_maze import *
from filler_utils import *

def filler_crops(state):
    return fill_rows(state, [dos, [
        [sense],
        [try_harvest],
        [Checker3, [plant_one, E.Tree], [plant_one, E.Carrot], [plant_one, E.Grass]],
    ]])

def filler_purge(state):
    return fill_rows(state, [try_harvest])

def filler_crop(state, e):
    return fill_rows(state, [dos, [
        [sense],
        [try_harvest],
        [plant_one, e]
    ]])


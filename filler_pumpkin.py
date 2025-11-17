from lib import *
from drones import *
from pumpkin import *
from filler_utils import *

def filler_pumpkin(state):
    def handler(state, results):
        state, d = wh(state)
        return do(state, [
            [try_harvest],
            [set_box_harvested, [0, 0, d, d]]
        ])
        
    return fill_rows(state, [do, [
        [plant_pumpkin, False],
    ]], handler)

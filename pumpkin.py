from lib import *
from harvest import *
from pattern import *
from planting import *
from sense import *    

def pumpkin_died(state):
    def done():
        return can_harvest() or get_entity_type() == E.Dead_Pumpkin
    while not done():
        pass
    return pure(state, not can_harvest())

def plant_pumpkin(state, do_fertilize=True):
    return do(state, [
        [sense],
        [cleanup],
        [water_to],
        [plant_one, E.Pumpkin],
        [when, do_fertilize, [dos, [
            [fertilize],
            [maybe_cure]
        ]]],
        [whenM, [pumpkin_died], [plant_pumpkin, do_fertilize]],
        [pure, True]
    ])

def Pumpkin(state, x, y, box, otherwise, do_fertilize=True, do_harvest=True):
    return do(state, [
        [Box, x, y, box,
            [dos, [
                [when, state["id"] == 0 and (x, y) == corner(box, SW), [dos, [
                    [when, do_harvest, [dos, [
                        [try_harvest, [E.Pumpkin]],
                        [set_box_harvested, box]
                    ]]]
                ]]],
                [plant_pumpkin, do_fertilize]
            ]],
            otherwise
        ]
    ])

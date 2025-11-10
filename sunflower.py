from lib import *
from harvest import *
from measure import *

def Sunflower(state, min_petals=7, max_petals=15, flags=[Sunflowers.WATER]):
    flags = set(flags)

    def valid_sunflower(state):
        return dos(state, [
            [bind, [get_here, "petals"], [pushret]],
            [condM, [lift1, [is_none], [peekret]],
                [dos, [
                    [popret],
                    [pure, False]
                ]],
                [lift2, [And],
                    [lift2, [GTE], [peekret], [pure(min_petals)]],
                    [lift2, [LTE], [popret], [pure(max_petals)]]
                ]
            ]
        ])

    return dos(state, [
        [sense],
        [when, Sunflowers.WATER in flags, [water_to]],
        [untilM, [valid_sunflower], [dos, [
            [harvestM],
            [plant_one, E.Sunflower]
        ]]],
        [when, Sunflowers.FERTILIZE in flags, [fertilize]]
    ])
        
def boost(state, n=1, min_petals=7, max_petals=15, flags=[Sunflowers.WATER, Harvesting.CURE, Harvesting.UNSAFE]):
    flags = set(flags)
    for _ in range(n):
        state = do_(state, [
            [Sunflower, min_petals, max_petals, flags],
            [wait_for_harvest],
            [try_harvest, [E.Sunflower], flags]
        ]) 
    return state
    
def boost_box(state, box, num_flowers=10, boosts=10, flags=[Sunflowers.WATER, Harvesting.CURE, Harvesting.UNSAFE]):
    flags = set(flags)
    i = 0
    [x0, y0, w, h] = box
    flowers = set()
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            flowers.add((x, y))
            i += 1
            if i == num_flowers:
                break
        if i == num_flowers:
            break
    state, (hx, hy) = xy(state)
    if (hx, hy) in flowers:
        return Sunflower(state, 7, 7, flags)
    else:
        return boost(state, boosts, flags)
        
def boost_solo(state):
    return dos(state, [
        [try_harvest],
        [Sunflower]
    ])

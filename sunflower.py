from lib import *
from harvest import *
from measure import *

def Sunflower(state, min_petals=7, max_petals=15, force=False, do_fertilize=False, do_water=True):
    state = sense(state)
    state = when(state,do_water, [water_to])
    while True:
        state, e = et(state)
        if force or e != E.Sunflower:
            state = do_(state, [
                [harvestM],
                [plant_one, E.Sunflower],
            ])
        state = sense(state)
        h = here(state)
        petals = h["petals"]
        if petals != None and petals >= min_petals and petals <= max_petals:
            break

    return when(state, do_fertilize, [fertilize])
        
def boost(state, n=1, do_fertilize=True, do_water=True, min_petals=7, max_petals=15, cure=True, unsafe=False):
    for _ in range(n):
        state = do_(state, [
            [Sunflower, min_petals, max_petals, True, do_fertilize, do_water],
            [wait_for_harvest],
            [try_harvest, [E.Sunflower], cure, unsafe]
        ]) 
    return state
    
def boost_box(state, box, num_flowers=10, boosts=10, force=False, do_fertilize=True, do_water=True):
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
    state, [hx, hy] = xy(state)
    if (hx, hy) in flowers:
        return Sunflower(state, 7, 7, force, do_fertilize)
    else:
        return boost(state, boosts, do_fertilize, do_water)
        
def boost_solo(state):
    return dos(state, [
        [try_harvest],
        [water_to],
        [Sunflower]
    ])

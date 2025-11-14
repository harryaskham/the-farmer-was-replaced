from farmlib import *
from filler_utils import *
from filler_cactus import *
from filler_pumpkin import *
from filler_energy import *

def filler_maze(state, num_drones=None):
    if num_drones == None:
        num_drones = max_drones()
    state, d = wh(state)
    n = d // ((num_drones ** 0.5) // 1)
    for y in range(n//2, n//2 + n * (d // n), n):
        for x in range(n//2, n//2 + n * (d // n), n):
            def child(state):
                return dos(state, [
                    [move_to, (d - 1 - x, d - 1 - y)],
                    [wait_secsM, 40],
                    [boxloop, [d-1-x, d-1-y, 1, 1], [maze, n]]
                ])
            state = spawn_(state, [child], [Spawn.FORK, Spawn.BECOME])
    return state


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
    
def filler_companions(state):
    
    def handler(state, results):
        state, d = wh(state)
        for result in values(results):
            for x, y in result:
                row = result[(x, y)]
                if x == d - 1:
                    for c in row:
                        state["grid"][(c["x"], c["y"])] = c
        return state
        
    return fill_rows(state, [dos, [
        [sense],
        [try_harvest, None, [Companions.AWAIT]],
        [Companion, [Checker3, [plant_one, E.Tree], [plant_one, E.Carrot], [plant_one, E.Grass]]],
        [sense],
        [get_row]
    ]], handler)

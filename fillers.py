from lib import *
from loops import *
from maze import *
from drones import *
from sunflower import *
from cactus import *
from filler_utils import *
from filler_cactus import *
from filler_pumpkin import *

def filler_maze(state, num_drones=None):
    if num_drones == None:
        num_drones = state["max_drones"]
    state, d = wh(state)
    n = d // ((num_drones ** 0.5) // 1)
    for y in range(n//2, n//2 + n * (d // n), n):
        for x in range(n//2, n//2 + n * (d // n), n):
            def child(state):
                return dos(state, [
                    [move_to, (x, y)],
                    [wait_secsM, 5],
                    [boxloop, [x, y, 1, 1], [maze, n]]
                ])
            state = spawn(state, [child], [Spawn.BECOME])
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
    
def filler_energy(state):
    state, d = wh(state)
    
    def sunflower_at(state, c):
        return spawnM(state, [dos, [
            [move_to, c],
            [Sunflower, 7, 7, [
                Sunflowers.WATER,
                Sunflowers.FERTILIZE,
                Harvesting.CURE,
                Harvesting.UNSAFE
            ]],
        ]])
        
    def boost_at(state, c):
        return spawnM(state, [dos, [
            [move_to, c],
            [forever, [boost, 10, True, True, 15, 15, True, True]]
        ]])

    def spaced(n=32, gap=1):
        cs = []
        for y in range(0, d, gap+1):
            for x in range(0, d, gap+1):
                cs.append((x, y))
                if len(cs) == n:
                    break
            if len(cs) == n:
                break
        return cs
        
    def sunflower_row(n=10):
        cs = []
        for x in range(n):
            cs.append([x, d-1])
        return cs
        
    def planter(state, y):
        return dos(state, [
            [boxloop, [0, y, d, 1], [dos, [
                [Sunflower, 7, 15]
            ]]]
        ])

    def harvester(state, y):
        state["petal_threshold"] = 15
        
        def decr(state):
            state["petal_threshold"] -= 1
            return state
            
        def reset(state):
            state["petal_threshold"] = 15
            return state
            
        def do_harv(state):
            state, h = get_here(state)
            petals = h["petals"]
            return pure(state, petals != None and petals >= state["petal_threshold"])

        return dos(state, [
            [boxloop, [0, y, d, 1], [dos, [
                [sense],
                [whenM, [do_harv], [dos, [
                    [try_harvest],
                    [reset]
                ]]],
                [whenM, [bind, [xy], [eq, [d-1, y]]], [decr]]
            ]]]
        ])
        
    return dos(state, [
        [mapM, [sunflower_at], sunflower_row()],
        [wait_all],
        [mapM, [boost_at], spaced()[1:]],
        [forever, [boost]]
    ])


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

from lib import *
from planting import *
from harvest import *
from sense import *
from move import *
from drones import *

def maze(state, size=None):
    state, start_pos = xy(state)
    state = sense(state)
    state, e = et(state)
    if et(state)[1] not in [E.Hedge, E.Treasure]:
        if size == None:
            state, size = wh(state)
        use_n = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
        state = do_(state, [
            [harvestM],
            [plant_one, E.Bush],
            [useM, I.Weird_Substance, use_n],
        ])

    seen = set()
    back = []
    while True:
        state = sense(state)
        
        if et(state)[1] == E.Treasure:
            state = do_(state, [
                [try_harvest, [E.Treasure]]
            ])
            break

        state, (x, y) = xy(state)
        seen.add((x, y))
        state, ns = neighbors_dict(state)
        moved = False
        
        ds = []       
        if state["treasure"][0] < x:
            ds.append(West)
        if state["treasure"][0] > x:
            ds.append(East)
        if state["treasure"][1] < y:
            ds.append(South)
        if state["treasure"][1] > y:
            ds.append(North)
        for d in [North, East, South, West]:
            ds.append(d)
            
        for d in ds:
            if d not in ns:
                continue
            n = ns[d]
            if n in seen:
                continue
            state, _ = moveM(state, d)
            if xy(state)[1] != (x, y):
                moved = True
                back.append(opposite(d))
                break
        if not moved:
            if back == []:
                break
            state, _ = moveM(state, back.pop())
            
    return move_to(state, start_pos)

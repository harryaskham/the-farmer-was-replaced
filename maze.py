from lib import *
from planting import *
from harvest import *
from sense import *
from move import *
from drones import *

def maze(state, size=None):
    state = Lock(state, "mk_maze")

    state = sense(state)
    state, e = et(state)
    if e not in [E.Hedge, E.Treasure]:
        if size == None:
            state, size = wh(state)
        use_n = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
        state = do_(state, [
            [harvestM],
            [plant_one, E.Bush],
            [useM, I.Weird_Substance, use_n],
        ])

    state = Unlock(state, "mk_maze")

    seen = set()

    def go(state, dir=None):
        state = sense(state)
        state, e = et(state)

        if state["treasure"] == None:
            return state

        if e == E.Treasure:
            return do_(state, [[try_harvest, [E.Treasure]]])

        state, (x, y) = xy(state)
        seen.add((x, y))
        state, ns = neighbors_dict(state)
        for d, n in items(ns):
            if n in seen:
                continue
            continuation = [whenM, [moveM, d, [Movement.FAST]], [go, d]]
            state, _ = spawn(state, continuation, [Spawn.FORK, Spawn.AWAIT])

    return go(state)

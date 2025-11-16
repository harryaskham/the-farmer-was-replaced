from lib import *
from planting import *
from harvest import *
from sense import *
from move import *
from drones import *

def add_seen(state, c):
    state = Lock(state, "maze_seen")
    seen = c in state["maze_seen"]
    state["maze_seen"].add(c)
    state = Unlock(state, "maze_seen")
    return pure(state, seen)

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
            [sense]
        ])

    state["maze_seen"] = set()

    state = Unlock(state, "mk_maze")

    def check_done(state, e):
        return pure(state, e == E.Treasure or e != E.Hedge or state["treasure"] == None)

    def next(dir):
        def continuation(state):
            return do_(state, [
                #[whenM, [moveM, dir, [Movement.FAST]], [go]]
                [whenM, [moveM, dir], [go]]
            ])
        return continuation

    def go(state):
        state, (x, y) = xy(state)
        state, seen = add_seen(state, (x, y))
        if seen:
            return state

        state, done = with_et(state, check_done)
        if done:
            return do_(state, [
                [try_harvest, [E.Treasure]],
            ])

        state, ns = neighbors_dict(state)
        ds = []
        state = Lock(state, "maze_seen")
        for dir, n in items(ns):
            if n in state["maze_seen"]:
                continue
            ds.append(dir)

        while len(ds) > 1:
            dir = ds.pop()
            state = spawn_(
                state,
                [next(dir)],
                [Spawn.SHARE, Spawn.AWAIT])

        state = Unlock(state, "maze_seen")

        if len(ds) == 0:
            return state
        return next(ds[0])(state)

    state = go(state)
    while True:
        wait_secs(1)
        state = sense(state)
        state, done = with_et(state, check_done)
        if done:
            break
    return state

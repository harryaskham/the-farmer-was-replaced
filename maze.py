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

    def add_seen(state, c):
        state = Lock(state, "seen")
        x = c not in seen
        if x:
            seen.add(c)
        state = Unlock(state, "seen")
        return pure(state, x)

    state, _ = add_seen(state, (x, y))

    def check_done(state, e):
        return pure(state, e == E.Treasure or e != E.Hedge or state["treasure"] == None)

    def go(state):
        state = sense(state)
        state, done = with_et(state, check_done)
        if done:
            return dos(state, [
                [try_harvest, [E.Treasure]],
                [pure, done]
            ])

        def next(dir):
            def continuation(state):
                return dos(state, [
                    [condM,
                        [moveM, dir, [Movement.FAST]],
                        [go],
                        [pure, False]
                    ]
                ])
            return continuation

        state, ns = neighbors_dict(state)
        ins = items(ns)
        ds = []
        for dir, n in ins:
            state, cont = add_seen(state, n)
            if not cont:
                continue
            ds.append(dir)

        if len(ds) == 0:
            return pure(state, False)

        for dir in ds[:-1]:
            state = spawn_(
                state,
                [next(dir)],
                [Spawn.FORK, Spawn.AWAIT])

        return next(ds[-1])(state)

    state, _ = go(state)
    while True:
        wait_secs(1)
        state, done = with_et(state, check_done)
        if done:
            break
    return state

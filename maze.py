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

    def go(state):
        state = sense(state)
        state, e = et(state)
        state, (x, y) = xy(state)

        if (e not in [E.Hedge, E.Treasure]) or (state["treasure"] == None):
            return pure(state, False)

        if (x, y) == state["treasure"]:
            return dos(state, [
                [try_harvest, [E.Treasure]],
                [pure, True]
            ])

        state, cont = add_seen(state, (x, y))
        if not cont:
            return pure(state, False)

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
        done = False
        for dir, n in ins:
            if n in seen:
                continue
            if dir == ins[-1][0]:
                state, done = next(dir)(state)
            else:
                state = spawn_(
                    state,
                    [next(dir)],
                    #[Spawn.SHARE, Spawn.AWAIT, Spawn.BECOME]) 
                    [Spawn.CLONE, Spawn.AWAIT, Spawn.BECOME]) 

        return pure(state, done)

    state, done = go(state)
    state, rs = wait_all(state)
    done = done or any(values(rs))
    return pure(state, done)

from lib import *
from planting import *
from harvest import *
from sense import *
from move import *
from drones import *

def add_seen(state, c):
    state = Lock(state, "maze_seen")
    seen = c in state["maze"]["seen"]
    state["maze"]["seen"].add(c)
    state = Unlock(state, "maze_seen")
    return pure(state, seen)

def use_substance(state, size):
    use_n = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
    return do_(state, [
        [useM, I.Weird_Substance, use_n]
    ])

def mk_maze(state, size=None):
    state = Lock(state, "maze_seen")
    state = Lock(state, "mk_maze")

    if size == None:
        state, size = wh(state)
    state = sense(state)
    state, e = et(state)
    state = do_(state, [
        [when, e not in [E.Hedge, E.Treasure], [do, [
            [harvestM],
            [plant_one, E.Bush],
        ]]],
        [use_substance, size],
        [sense]
    ])

    state["maze"]["seen"] = set()

    state = Unlock(state, "mk_maze")
    state = Unlock(state, "maze_seen")

    return state

def maze(state, size=None, limit=0):

    def next(dir):
        def continuation(state):
            return state.do_([
                [whenM, [moveM, dir, [Movement.FAST]], [go]]
            ])
        return continuation

    def handle_treasure(state, t):
        return state.do([
            [cond, t == None,
                [pure, True],
                [condM, [eqM, [xy], [pure, t]],
                    [do, [
                        [clear_treasure],
                        [condM, [incr_maze, limit],
                            [use_substance, size],
                            [harvestM],
                        ],
                        [sense],
                        [pure, True]
                    ]],
                    [pure, False]
                ]
            ]
        ])

    def check_done(state):
        return state.do([
            [sense],
            [condM, [then, [lift([Contains]), [E.Hedge, E.Treasure]], [et]],
                [with_treasure, handle_treasure],
                [pure, True],
            ]
        ])

    def go(state):
        state = sense(state)
        state, (x, y) = xy(state)
        state, seen = add_seen(state, (x, y))
        if seen:
            return state

        state, done = check_done(state)
        if done:
            return state

        state, ns = neighbors_dict(state)
        ds = []
        state = Lock(state, "maze_seen")
        for dir, n in items(ns):
            if n in state["maze"]["seen"]:
                continue
            ds.append(dir)

        while len(ds) > 1:
            state = spawn_(
                state,
                [next(ds.pop())],
                [Spawn.SHARE, Spawn.BECOME, Spawn.EXCURSE])

        state = Unlock(state, "maze_seen")

        if len(ds) == 0:
            return state
        return next(ds.pop())(state)

    state = mk_maze(state, size)
    state = go(state)

    def check(state):
        return num_drones() == 1

    while not state.only_drone().eval():
        wait_secs(5)
        state.dump(info)

    if state["maze"]["count"] < limit:
        return do_(state, [
            [mk_maze, size],
            [go]
        ])

    return state

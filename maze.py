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

def maze(state, size, limit):

    def next(dir):
        def continuation(state):
            state, c = xy(state)
            return state.do([
                [condM, [moveM, dir, [Movement.FAST]],
                    [do, [
                        [map_direction, c, dir, True],
                        go
                    ]],
                    [do, [
                        [map_direction, c, dir, False],
                        [pure, False]
                    ]]
                ]
            ])
        return continuation

    def handle_treasure(state, t):
        return state.do([
            [cond, t == None,
                [pure, True],
                [condM, [eqM, [xy], [pure, t]],
                    [do, [
                        [clear_treasure],
                        [cond, state["maze"]["count"] < limit,
                            [use_substance, size],
                            [harvestM]
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

    go = [do, [
        [sense],
        [condM, [bind, [xy], [add_seen]],
            [pure, False],
            [condM, check_done,
                [pure, True],
                [dos, [
                    [flapM, [neighbors_dict], [pipeM,
                        [lift([values])],
                        [lift([map]), pipe(singleton, next)],
                        [mapM, [flipM, spawn, [Spawn.FORK, Spawn.MERGE, Spawn.BECOME, Spawn.EXCURSE]]]
                    ]],
                    [fmap, pipe(values, any), [wait_all]]
                ]]
            ]
        ]
    ]]

    cont = True
    while cont:
        state, done = state.do([
            [mk_maze, size],
            go,
            #[dump, info],
        ])
        if done:
            state, cont = incr_maze(state, limit)
    return reset_maze(state)

from lib import *
from planting import *
from harvest import *
from sense import *
from move import *
from drones import *
import List
import Map

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

    def search_maze(state, dir):
        def continuation(state):
            state, c = xy(state)
            return state.do([
                [condM, [moveM, dir, [Movement.FAST]],
                    [do, [
                        [map_direction, c, dir, True],
                        search_go
                    ]],
                    [do, [
                        [map_direction, c, dir, False],
                        [pure, False]
                    ]]
                ]
            ])
        return pure(state, [continuation])

    def map_maze(state, dir):
        def continuation(state):
            state, c = xy(state)
            return state.do([
                [condM, [moveM, dir, [Movement.FAST]],
                    [do, [
                        [map_direction, c, dir, True],
                        map_go
                    ]],
                    [map_direction, c, dir, False],
                ]
            ])
        return pure(state, [continuation])

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

    def find_treasure(state):
        return state.do([
            [sense],
            [condM, [then, [lift([Contains]), [E.Hedge, E.Treasure]], [et]],
                [with_treasure, handle_treasure],
                [pure, True],
            ]
        ])

    def mapping_done(state):
        return pure(state, False)

    MAP_FLAGS = [
        Spawn.FORK,
        Spawn.MERGE,
        Spawn.WAIT_AFTER,
        Spawn.BECOME,
        Spawn.EXCURSE
    ]

    SEARCH_FLAGS = [
        Spawn.FORK,
        Spawn.MERGE,
        Spawn.WAIT_AFTER,
        Spawn.BECOME,
        Spawn.EXCURSE
    ]

    def mk_go(mk_continuation, check_done, flags):
        return [do, [
            [sense],
            [unlessM, [bind, [xy], [add_seen]],
                [unlessM, [check_done],
                    [flipM, mapM, Dirs, [pipeM(
                        [mk_continuation],
                        [flipM, spawn, flags]
                    )]],
                ]
            ]
        ]]

    map_go = mk_go(map_maze, mapping_done, MAP_FLAGS)
    search_go = mk_go(search_maze, find_treasure, SEARCH_FLAGS)

    return state.do([
        [whileM, [incr_maze, limit], [do, [
            [mk_maze, size],
            map_go,
            #search_go,
            #[fmap, [pipe(values, any)], [wait_all]],
            [wait_all],
            [dump, info]
        ]]],
        [wait_secsM, 1000],
        [reset_maze]
    ])

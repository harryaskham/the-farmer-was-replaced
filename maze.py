from lib import *
from planting import *
from harvest import *
from sense import *
from move import *
from drones import *
import List
import Map
import State

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

    def map_maze(dir):
        return [do, [
            [whenM, [moveM, dir, [Movement.FAST]],
                [do, [
                    [map_direction, dir],
                    [go, map_maze, mapping_done, MAP_FLAGS],
                ]],
            ]
        ]]

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
        Spawn.SHARE,
        Spawn.AWAIT,
    ]

    def go(state, mk_continuation, check_done, flags):
        return state.do([
            [sense],
            [unlessM, [bind, [xy], [add_seen]],
                [unlessM, [check_done], [do, [
                    [forM, map(mk_continuation, Dirs[:-1]), [flipM, spawn, flags]],
                    mk_continuation(Dirs[-1]),
                ]]],
            ],
            [wait_returns],
        ])

    return state.do([
        [whileM, [incr_maze, limit], [do, [
            [mk_maze, size],
            [go, map_maze, mapping_done, MAP_FLAGS],
            [bind, [State.get, "maze"], [info]],
        ]]],
        #[reset_maze]
    ])

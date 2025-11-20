from lib import *
from planting import *
from harvest import *
from sense import *
from move import *
from drones import *
import State

def add_seen(state, c):
    state = Lock(state, "maze_seen")
    seen = c in state["maze"]["seen"]
    state["maze"]["seen"].add(c)
    state = Unlock(state, "maze_seen")
    return pure(state, seen)

def is_seen(state, c):
    return pure(state, c in state["maze"]["seen"])

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

def go_dir(dir):
    def f(state):
        return state.do([
            [unlessM, [bind, [xy], [add_seen]], [do, [
                [whenM, [moveM, dir], [do, [
                    [map_direction, dir],
                    [go]
                ]]]
            ]]],
        ])
    return [f]

go_dirs = map(go_dir, Dirs)

def go(state):
    return state.do([
        [sense],
        [spawns, go_dirs],
    ])

def maze(state, size, limit):

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
        ] )

    def find_treasure(state):
        return state.do([
            [sense],
            [condM, [then, [lift([Contains]), [E.Hedge, E.Treasure]], [et]],
                [with_treasure, handle_treasure],
                [pure, True],
            ]
        ])

    state = state.do_([
        [whileM, [incr_maze, limit], [do, [
            [mk_maze, size],
            [go],
            #[wait_all_solo]
            [wait_all]
        ]]],
        #[reset_maze]
    ])
    state = dump(state)
    return state

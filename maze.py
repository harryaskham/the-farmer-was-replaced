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

def map_dir(dir):
    def f(state):
        return state.do([
            [unlessM, [bind, [xy], [add_seen]], [do, [
                [whenM, [moveM, dir], [do, [
                    [map_direction, dir],
                    [map_maze]
                ]]]
            ]]],
        ])
    return [f]

map_dirs = map(map_dir, Dirs)

def map_maze(state):
    return state.do([
        [sense],
        [spawns, map_dirs],
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

    def default_get_target(state):
        return state["maze"]["treasure"]

    def pathM(state, c=None, get_target=default_get_target, path=None):
        state = sense(state)

        state["maze"]["seen"] = set()

        if c == None:
            state, c = xy(state)

        target = get_target(state)

        if path == None:
            path = []

        q = [(c, [])]

        while q != []:
            state = sense(state)
            if get_target(state) != target:
                return pure(state, None)

            (c, path), q = q[0], q[1:]
            if c == target:
                return pure(state, path)
            if c in state["maze"]["seen"]:
                return pure(state, None)
            state["maze"]["seen"].add(c)
            for dir in Dirs:
                state, cn = pos_to(state, dir, c)
                if cn in state["maze"]["seen"]:
                    continue
                if (c, cn) not in state["maze"]["map"]:
                    continue
                path_n = list(path)
                path_n.append(dir)
                q.append((cn, path_n))
        return pure(state, None)

    def populate_all_paths(state):
        state, d = wh(state)
        for y in range(d):
            for x in range(d):
                c = (x, y)
                for y_ in range(d):
                    for x_ in range(d):
                        n = (x_, y_)
                        state = info(state, ("Computing path", c, "to", n))
                        if n == None or ((c, n) in state["maze"]["all_paths"]):
                            continue
                        def get_target(state):
                            return n
                        state, path = pathM(state, c, get_target)
                        if path == None:
                            return fatal(state, ("No path found in maze from", c, "to", n))
                        state = info(state, ("Populated path", c, "to", n))
                        state["maze"]["all_paths"][(c, n)] = path
                        state["maze"]["all_paths"][(n, c)] = reverse(map(opposite, path))
        return state

    def get_path(state):
        t = state["maze"]["treasure"]
        state, c = xy(state)
        return pure(state, state["maze"]["all_paths"][(c, t)])

    def grow_maze(state, harvest=False):
        return state.do_([
            [bind, [get_path], [mapM, [moveM]]],
            [cond, harvest,
                [harvestM],
                [use_substance, size]],
            [sense]
        ])

    def grow_limit(state, limit):
        return state.do_([
            [whileM, [incr_maze, limit], [do, [
                [grow_maze],
                [bind, [bind, [State.get, "maze"], [flipM, lift([getattr]), "count"]], [info]]
            ]]],
        ])

    def finish_maze(state):
        return state.do_([
            [grow_maze, True],
        ])

    return state.do_([
        [reset_maze],
        [mk_maze, size],
        [map_maze],
        [wait_all],
        [populate_all_paths],
        [grow_limit, limit],
        [finish_maze]
    ])

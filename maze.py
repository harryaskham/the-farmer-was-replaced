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
    return state

def map_dir(dir, drone_limit=None):
    def f(state):
        return state.do([
            [whenM, [moveM, dir], [do, [
                [unlessM, [bind, [xy], [add_seen]], [do, [
                    [map_direction, dir],
                    [map_maze, drone_limit]
                ]]]
            ]]]
        ])
    return [f]

def map_dirs(state, drone_limit=None):
    ds = []
    for dir in Dirs:
        ds.append(map_dir(dir, drone_limit))
    return state.do([
        [when, ds != [], [spawns, ds, drone_limit]]
    ])

def map_maze(state, drone_limit=None):
    return state.do([
        [map_dirs, drone_limit],
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

    q = [(c, [], set())]

    while q != []:
        state = sense(state)
        if get_target(state) != target:
            return pure(state, None)

        #(c, path, seen), q = q[0], q[1:]
        (c, path, seen) = q.pop()

        if c == target:
            return pure(state, path)
        if c in seen:
            return pure(state, None)
        seen = set(seen)
        seen.add(c)
        for dir in Dirs:
            state, cn = pos_to(state, dir, c)
            if cn in seen:
                continue
            if (c, cn) not in state["maze"]["map"]:
                continue
            path_n = list(path)
            path_n.append(dir)
            q.append((cn, path_n, seen))
    return pure(state, None)

def populate_paths_from(state, start):
    state["maze"]["seen"] = set()
    q = [(start, [])]
    while q != []:
        (c, path), q = q[0], q[1:]
        if c in state["maze"]["seen"]:
            continue
        state["maze"]["seen"].add(c)
        if (start, c) not in state["maze"]["all_paths"]:
            state["maze"]["all_paths"][(start, c)] = list(path)
        if (c, start) not in state["maze"]["all_paths"]:
            state["maze"]["all_paths"][(c, start)] = reverse(map(opposite, path))
        for dir in Dirs:
            state, cn = pos_to(state, dir, c)
            if cn in state["maze"]["seen"]:
                continue
            if (c, cn) not in state["maze"]["map"]:
                continue
            path_n = list(path)
            path_n.append(dir)
            q.append((cn, path_n))
    return state

def populate_all_paths(state):
    state = info(state, ("Computing paths"))
    state = info(state, state["maze"])
    state, d = wh(state)
    for y in range(d):
        for x in range(d):
            start = (x, y)
            state = info(state, ("Computing paths from", start))
            state = populate_paths_from(state, start)
    state = info(state, ("Computed paths"))
    state = info(state, state["maze"])
    return state

def populate_all_paths_2(state):
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
    if (c, t) in state["maze"]["all_paths"]:
        return pure(state, state["maze"]["all_paths"][(c, t)])
    else:
        return pathM(state, c)

def grow_maze(state, size, harvest=False):
    return state.do_([
        [bind, [get_path], [mapM, [moveM]]],
        [cond, harvest,
            [harvestM],
            [use_substance, size]],
        [sense]
    ])

def grow_limit(state, size, limit):
    return state.do_([
        [whileM, [incr_maze, limit], [do, [
            [grow_maze, size],
            [bind, [bind, [State.get, "maze"], [flipM, lift([getattr]), "count"]], [info]]
        ]]],
    ])

def finish_maze(state, size):
    return state.do_([
        [grow_maze, size, True],
    ])

def maze(state, size, limit, drone_limit=max_drones()):
    return state.do_([
        [reset_maze],
        [mk_maze, size],
        [map_maze, drone_limit],
        [wait_all],
        [populate_all_paths],
        [grow_limit, size, limit],
        [finish_maze, size]
    ])

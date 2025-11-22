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
        [useM, I.Weird_Substance, use_n, False]
    ])

def mk_maze(state, size=None, force=True):
    if size == None:
        state, size = wh(state)
    state = sense(state)
    state, e = et(state)
    if e in [E.Hedge, E.Treasure] and not force:
        return state
    state = do_(state, [
        [when, e not in [E.Hedge, E.Treasure], [do, [
            [harvestM],
            [plant_one, E.Bush],
        ]]],
        [use_substance, size],
        [sense]
    ])
    state["maze"]["seen"] = set()
    state, c = xy(state)
    state["maze"]["start"] = c
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

def map_to_dir(dir):
    def f(state):
        return state.do([
            [map_maze_solo, dir]
        ])
    return [f]
map_workers = map(map_to_dir, Dirs)

def map_all_dirs(state):
    state["maze"]["seen"] = set()
    return state.do_([
        [spawns, map_workers]
    ])

def map_maze_solo(state, dir=None, start=None, path=None):
    state, c = xy(state)
    if start == None:
        start = c
    if path == None:
        path = []
    state, seen = add_seen(state, c)
    state = add_all_paths(state, start, c, path)
    if seen:
        return state
    ds = Dirs
    if dir != None:
        ds = [dir]
    for dir in ds:
        state, n = pos_to(state, dir)
        state, seen = is_seen(state, n)
        if seen:
            continue
        state, moved = moveM(state, dir)
        if moved:
            path_n = list(path)
            path_n.append(dir)
            state = map_direction(state, dir)
            state = map_maze_solo(state, None, start, path_n)
            state, _ = moveM(state, opposite(dir))
    return state

def default_get_target(state):
    return state["maze"]["treasure"]

def mk_target(t):
    def f(state):
        return t
    return f

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

def add_one_path(state, a, b, path):
    if (
        (a, b) not in state["maze"]["all_paths"]
        or len(state["maze"]["all_paths"][(a, b)]) > len(path)
    ):
        state["maze"]["all_paths"][(a, b)] = path
    return state

def add_path(state, a, b, path):
    state["maze"]["all_paths"][(a, a)] = []
    state["maze"]["all_paths"][(b, b)] = []
    add_one_path(state, a, b, path)
    return state

def add_all_paths(state, start, end, path):
    #add_path(state, start, end, path)
    s = start
    for i, dir in enumerate(path):
        add_path(state, s, end, path[i:])
        #e = end
        #for j in range(len(path)-1, i-1, -1):
        #    add_path(state, s, e, path[i:j+1])
        #    break
        #    state, e = pos_to(state, opposite(path[j]), e)
        state, s = pos_to(state, dir, s)
    return state

def populate_paths(state, size, start=None):
    state["maze"]["seen"] = set()
    if start == None:
        start = (size // 2, size // 2)
    q = [(start, [])]
    while q != []:
        state = info(state, ("Populating paths, queue size", len(q), "seen size", len(state["maze"]["seen"])))
        (c, path) = q.pop()

        state, seen = add_seen(state, c)
        if seen:
            continue

        state = add_all_paths(state, start, c, path)

        for dir in Dirs:
            state, cn = pos_to(state, dir, c)
            if cn in state["maze"]["seen"]:
                continue
            if not ((c, cn) in state["maze"]["map"] or ((cn, c) in state["maze"]["map"])):
                continue
            path_n = list(path)
            path_n.append(dir)
            q.append((cn, path_n))
    return state

def populate_all_paths(state, size):
    state = info(state, ("Computing paths"))
    state = info(state, state["maze"])
    for y in range(size):
        for x in range(size):
            start = (x, y)
            state = info(state, ("Computing paths from", start))
            state = populate_paths(state, size, start)
    state = info(state, ("Computed paths"))
    state = info(state, state["maze"])
    return state

def get_path(state, t=None, c=None):
    while t == None:
        state = sense(state)
        t = state["maze"]["treasure"]
        if t != None:
            break
        wait_secs(state["delay"])

    if c == None:
        state, c = xy(state)

    state = debug(state, ("Getting path from", c, "to", t))

    if c == t:
        return pure(state, [])
    if (c, t) in state["maze"]["all_paths"]:
        return pure(state, state["maze"]["all_paths"][(c, t)])
    elif (t, c) in state["maze"]["all_paths"]:
        return pure(state, reverse(map(opposite, state["maze"]["all_paths"][(t, c)])))
    else:
        start = state["maze"]["start"]
        state, path = get_path(state, start, c)
        state, rest = get_path(state, t, start)
        path = list(path)
        for dir in rest:
            path.append(dir)
        return pure(state, path)

        #state = warn(state, ("Computing path on the fly from", c, "to", t))
        #return pathM(state, c, mk_target(t))
        #return fatal(state, ("No path stored from", c, "to", t))

def maze_move_to(state, c):
    state, path = get_path(state, c)
    return fast_follow(state, path)

def fast_follow(state, path):
    for dir in path:
        move(dir)
    return sense_position(state)

def abortive_follow(state, path, ):
    state = sense(state)
    t = state["maze"]["treasure"]
    success = True
    for dir in path:
        state, moved = state.do([
            [delay_lock, [same_treasure, t], [moveM, dir], 0]
        ])
        if not moved:
            success = False
            break
    return pure(state, success)

def lock_treasure(state):
    state = sense(state)
    state, c = xy(state)
    return pure(state, state["maze"]["treasure"] == c)

def same_treasure(state, t):
    state = sense(state)
    return pure(state, state["maze"]["treasure"] == t)

def delay_path(state):
    state, path = get_path(state)
    wait_secs(len(path) / 10.0)
    return pure(state, path)

def grow_maze(state, size, harvest=False):
    state = sense(state)
    t = state["maze"]["treasure"]
    #state, path = delay_path(state)
    state, path = get_path(state)
    return state.do_([
        #[delay_lock, [same_treasure, t], [do, [
            [fast_follow, path],
            #[delay_lock, [same_treasure, t], [do, [
                [cond, harvest,
                    [harvestM],
                    [use_substance, size]]
                #]], 0]
                #]], 0]
    ])

def soloM(state):
    return pure(state, num_drones() == 1)

def everyN(state, n, max=None):
    if max == None:
        max = 300
    count = state["maze"]["count"]
    return pure(state, count < max and count % n == 0)

def reset_seen(state):
    state["maze"]["seen"] = set()

def grow_limit(state, size, limit):
    return state.do_([
        [whileM, [incr_maze, limit], [do, [
            [grow_maze, size],
            #[whenM, [everyN, 20], [do, [
            #[whenM, [soloM], [do, [
            #    [wait_all],
            #    [reset_seen],
            #    [spawn, [map_maze_solo]]
            #]]],
            [then, [info],
                [liftA2, [pairM],
                    [State.get, "id"],
                    [bind, [State.get, "maze"], [flipM, lift([getattr]), "count"]]]]
        ]]]
    ])

def finish_maze(state, size):
    return state.do_([
        [grow_maze, size, True],
    ])

def maze(state, size, limit, drone_limit=max_drones()):
    return state.do_([
        [reset_maze],
        [mk_maze, size],
        [map_maze_solo],
        [grow_limit, size, limit],
        [finish_maze, size]
    ])

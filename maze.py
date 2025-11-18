from lib import *
from planting import *
from harvest import *
from sense import *
from move import *
from drones import *

def add_seen(state, c):
    state = Lock(state, "maze_seen")
    seen = c in state["maze_status"]["seen"]
    state["maze_status"]["seen"].add(c)
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

    state["maze_status"]["seen"] = set()

    state = Unlock(state, "mk_maze")
    state = Unlock(state, "maze_seen")

    return state

def maze(state, size=None, reuse_limit=0):

    def next(dir):
        def continuation(state):
            return do_(state, [
                [whenM, [moveM, dir, [Movement.FAST]], [go]]
            ])
        return continuation

    def check_done(state):
        state = sense(state)
        state, e = et(state)
        if e not in (E.Hedge, E.Treasure):
            return pure(state, True)

        state, has_t = has_treasure(state)
        if not has_t:
            return pure(state, True)

        state, t = get_treasure(state)
        state, c = xy(state)
        if t == c:
            state["maze_status"]["reuse_count"] += 1
            if state["maze_status"]["reuse_count"] < reuse_limit + 1:
                return do(state, [
                    [use_substance, size],
                    [pure, True]
                ])
            else:
                return do(state, [
                    [harvestM],
                    [pure, True]
                ])

        return pure(state, False)

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
            if n in state["maze_status"]["seen"]:
                continue
            ds.append(dir)

        while len(ds) > 1:
            dir = ds.pop()
            state = start_excursion(state)
            state = spawn_or(
                state,
                [next(dir)],
                [Spawn.SHARE])
            state = end_excursion(state)

        state = Unlock(state, "maze_seen")

        if len(ds) == 0:
            return state
        return next(ds.pop())(state)

    state = mk_maze(state, size)
    state = go(state)

    def check(state):
        return state["num_drones"] == 1

    done = False
    while not done:
        wait_secs(1)
        state, done = with_drone_state(state, check)

    if state["maze_status"]["reuse_count"] < reuse_limit:
        return do_(state, [
            [mk_maze, size],
            [go]
        ])

    return state

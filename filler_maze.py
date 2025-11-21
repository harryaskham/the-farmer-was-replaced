from farmlib import *
from filler_utils import *

def filler_maze(state):
    state, d = wh(state)
    size = 5
    starts = []
    tasks = []
    for x in range(size // 2, d - size // 2, size):
        for y in range(size // 2, d - size // 2, size):
            starts.append((x, y))
    for start in starts:
        tasks.append([do, [
            [move_to, start],
            [wait_secsM, 10],
            [forever, [maze, size, 300]]
        ]])
    state = state.do_([
        [spawns, tasks[1:32]],
        tasks[0]
    ])

def filler_maze_large(state):
    state, d = wh(state)

    def in_maze(state):
        state = sense(state)
        state, e = et(state)
        return pure(state, e in [E.Hedge, E.Treasure])

    def map_to_dir(dir):
        return [do, [
            [bind, [xy], [add_seen]],
            [whenM, [moveM, dir], [do, [
                [map_direction, dir],
                [map_maze_solo]
            ]]]
        ]]

    def worker(start):
        return [do, [
            #[maze_move_to, start],
            [move_to, start],
            [wait_secsM, 30],
            [map_maze_solo],
            [whileM, [in_maze], [grow_maze, d, False]]
        ]]

    workers = []
    size = 5
    for x in range(size // 2, d - size // 2, size):
        for y in range(size // 2, d - size // 2, size):
            workers.append(worker((x, y)))

    state = state.do_([
        [forever, [do, [
            [move_to, (d//2, d//2)],
            [reset_maze],
            [mk_maze, d],
            [spawns, workers[:31]],
            [map_maze_solo],
            #[populate_paths, d],
            #[spawns, workers[:31]],
            [grow_limit, d, 300],
            [sense],
            [finish_maze, d],
            [wait_all]
        ]]]
    ])

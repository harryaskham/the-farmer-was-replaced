from farmlib import *
from filler_utils import *
import State

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

    def worker(c):
        return [forever, [do, [
            [move_to, c],
            [reset_maze],
            [wait_secsM, 10],
            [mk_maze, size],
            [map_maze_solo],
            [grow_limit, size, 300],
            [sense],
            [finish_maze, d],
        ]]]

    workers = []
    size = 10
    for x in range(size // 2, d, size):
        for y in range(size // 2, d, size):
            workers.append(worker((x, y)))

    return state.do_([
        [spawns, workers[1:]],
        workers[0]
    ])

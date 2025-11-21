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
    state = state.do([spawns, tasks[1:]])
    state = state.do(tasks[0])

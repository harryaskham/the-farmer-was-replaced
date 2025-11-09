from lib import *

def cache_loop(state, loop):
    loops = []
    for y in range(wh(state)):
        row = []
        for x in range(wh(state)):
            row.append(loop(state, x, y))
        loops.append(row)
    def cached(state, x, y):
        return loops[y][x]
    return cached
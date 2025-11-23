from lib import *
from loops import *
from drones import *

def get_row(state):
    state, d = wh(state)
    state, (x, y) = xy(state)
    cs = []
    for x in range(d):
        state, c = at(state, (x, y))
        cs.append(c)
    return pure(state, cs)

def result_list(state, results):
    xs = []
    for child_id in results:
        xs.append(results[child_id])
    return pure(state, xs)

def merge_rows(state, results):
    return mapM(state, [merge_row], values(results))

def merge_row(state, row):
    return mapM(state, [merge_cell], row)

def merge_cell(state, cell):
    state["grid"][(cell["x"], cell["y"])] = cell
    return state

def fill_row(state, f, handler=None, flags=[], n=None):
    if n == None:
        n = state["max_drones"]
    state, d = wh(state)
    def p(y):
        return [boxloop, [0, y, d, 1], f, [0, y], False]
    for y in range(1, min(d, n)):
        state = spawn_(state, p(y), flags)
    state, results0 = do(state, [p(0)])
    if handler == None:
        return state
    state, results = wait_all(state)
    results[state["id"]] = results0
    for i in results:
        box_results = results[i]
        for c in box_results:
            cell_results = box_results[c]
            state = apply(state, handler, cell_results)
    return state

def fill_grid(
    state,
    f,
    cell_handler=None,
    final_handler=None,
    flags=[Spawn.FORK, Spawn.BECOME],
    n=None):
    flags = set(flags)

    if n == None:
        n = state["max_drones"]

    state, d = wh(state)

    def p(y):
        return [boxloop, [0, y, d, 1], f, [0, y], False]

    for y in range(1, min(d, n)):
        state = spawn_(state, p(y), flags)

    state, results0 = do(state, [p(0)])
    state, results = wait_all(state)
    results[state["id"]] = results0

    if cell_handler != None:
        for i in results:
            box_results = results[i]
            for c in box_results:
                cell_results = box_results[c]
                state = cell_handler(state, cell_results)

    if final_handler != None:
        state = final_handler(state)

    return state

def fill_rows(state, f, handler=None, n=None):
    if n == None:
        n = state["max_drones"]
    state, d = wh(state)
    def p(y):
        return [boxloop, [0, y, d, 1], f, [0, y], False]
    for y in range(1, min(d, n)):
        state = spawn_(state, p(y))
    state, results0 = do(state, [p(0)])
    if handler == None:
        return state
    state, results = wait_all(state)
    results[state["id"]] = results0
    return handler(state, results)

def fill_rowsM(state, f, handler, n=None):
        def h(state, results):
                return do(state, [
                        [pushret, results],
                        handler
                ])
        return fill_rows(state, f, h, n)

OSCILLATE_FLAGS = [Spawn.FORK, Movement.LOOP]

def oscillate(state, ltr, rtl, flags=OSCILLATE_FLAGS):
    state, d = wh(state)
    flags = set(flags)

    def repeat_dir(state, f, dir, n):
        for i in range(n):
            state = state.do_([
                f,
                [moveM, dir]
            ])
        return state
    def p(y):
        def go(state):
            inner = [do, [
                [repeat_dir, ltr, East, d-1],
                [repeat_dir, rtl, West, d-1],
            ]]
            if Movement.LOOP in flags:
                return state.do([
                    [move_to, (0, y)],
                    [forever, inner]
                ])
            else:
                return state.do([
                    move_to, (0, y),
                    inner
                ])
        return [go]

    workers = []
    for y in range(d-1, 0, -1):
        workers.append(p(y))
    return state.do([
        [spawns, workers[1:]],
        p(0)
    ])

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
    state, results0 = dos(state, [p(0)])
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

    state, results0 = dos(state, [p(0)])
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
    state, results0 = dos(state, [p(0)])
    if handler == None:
        return state
    state, results = wait_all(state)
    results[state["id"]] = results0
    return handler(state, results)

def fill_rowsM(state, f, handler, n=None):
        def h(state, results):
                return dos(state, [
                        [pushret, results],
                        handler
                ])
        return fill_rows(state, f, h, n)

OSCILLATE_FLAGS = [Spawn.FORK, Spawn.BECOME, Movement.LOOP]

def oscillate(state, ltr, rtl, flags=OSCILLATE_FLAGS):
    state, d = wh(state)
    flags = set(flags)
    ltr_flags = without(flags, Movement.LOOP)
    rtl_flags = toggle(ltr_flags, Movement.REVERSE)

    def p(y):
        b = row_box(d, y)
        inner = [dos, [
            [box_do, b, ltr, ltr_flags],
            [box_do, b, rtl, rtl_flags]
        ]]
        if Movement.LOOP in flags:
            return [forever, inner]
        else:
            return inner

    for y in range(d-1, 0, -1):
        state = spawn_(state, p(y), flags)
        if Spawn.SERIAL in flags:
            state, _ = wait_all(state)

    return dos(state, [p(0)])

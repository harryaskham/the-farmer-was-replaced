from lib import *
from excursion import *
from sense import *

def moveM(state, d, flags=[]):
    flags = set(flags)
    state, prev = xy(state)

    if not move(d):
        return pure(state, False)

    state = do_(state, [
        [sense, flags],
        [unless, Movement.REWIND_EXCURSION in flags, [maybe_update_excursion, d]]
    ])

    if Dinosaur.UPDATE_TAIL in flags:
        state["tail"].append(prev)
        if len(state["tail"]) > state["tail_len"]:
            if state["tail"][0] in state["tail_set"]:
                state["tail_set"].remove(state["tail"][0])
            state["tail"] = state["tail"][1:]
        state["tail_set"].add(prev)

    return pure(state, True)

def move_bounded(state, dir, flags=[]):
    flags = set(flags)
    state, [x, y] = xy(state)
    state, d = wh(state)
    if x == d-1 and dir == East:
        return pure(state, False)
    if x == 0 and dir == West:
        return pure(state, False)
    if y == d-1 and dir == North:
        return pure(state, False)
    if y == 0 and dir == South:
        return pure(state, False)
    return moveM(state, dir, flags)

def move_to(state, c):
    cx, cy = unpack(c)

    while x(state)[1] > cx:
        state, moved = moveM(state, West)
        if not moved:
            fatal(state, "Couldn't move")

    while x(state)[1] < cx:
        state, moved = moveM(state, East)
        if not moved:
            fatal(state, "Couldn't move")

    while y(state)[1] > cy:
        state, moved = moveM(state, South)
        if not moved:
            fatal(state, "Couldn't move")

    while y(state)[1] < cy:
        state, moved= moveM(state, North)
        if not moved:
            fatal(state, "Couldn't move")

    return state

def end_excursion(state):
    excursion = state["excursions"].pop()
    while excursion != []:
        d = excursion.pop()
        state, _ = moveM(state, opposite(d), [Movement.REWIND_EXCURSION])
    return state

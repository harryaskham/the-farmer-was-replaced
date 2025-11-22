from lib import *
from excursion import *
from sense import *

CW = {
    North: East,
    East: South,
    South: West,
    West: North
}

CCW = {
    North: West,
    West: South,
    South: East,
    East: North
}

Rots = [CW, CCW]

MOVE_FLAGS = set([
    Movement.FAST,
    Movement.UNBOUNDED,
])

def moveM(state, d, flags=MOVE_FLAGS):
    if Movement.FAST in flags:
        if state["has_excursion"] != None:
            state = warn(state, "FAST movement during excursion")
        moved = move(d)
        state = sense_position(state)
        return pure(state, moved)

    flags = set(flags)
    state, prev = xy(state)
    if Movement.UNBOUNDED in flags:
        moved = move(d)
    else:
        state, moved = move_bounded(state, d)

    if moved and Movement.REWIND_EXCURSION not in flags:
        state = maybe_update_excursion(state, d)

    return do(state, [
        [sense, flags],
        [when, Dinosaur.UPDATE_TAIL in flags, [update_dinosaur_tail, prev, d]],
        [pure, moved]
    ])

def update_dinosaur_tail(state, prev, d):
    state["tail"].append(prev)
    if len(state["tail"]) > state["tail_len"]:
        if state["tail"][0] in state["tail_set"]:
            state["tail_set"].remove(state["tail"][0])
        state["tail"] = state["tail"][1:]
    state["tail_set"].add(prev)
    return state

def move_bounded(state, dir, flags=MOVE_FLAGS):
    state, (x, y) = xy(state)
    state, d = wh(state)
    if x == d-1 and dir == East:
        return pure(state, False)
    if x == 0 and dir == West:
        return pure(state, False)
    if y == d-1 and dir == North:
        return pure(state, False)
    if y == 0 and dir == South:
        return pure(state, False)
    return moveM(state, dir, without(flags, Movement.UNBOUNDED))

def move_to(state, c, flags=MOVE_FLAGS):
    cx, cy = unpack(c)

    while x(state)[1] > cx:
        state, moved = moveM(state, West, flags)
        if not moved:
            fatal(state, "Couldn't move")

    while x(state)[1] < cx:
        state, moved = moveM(state, East, flags)
        if not moved:
            fatal(state, "Couldn't move")

    while y(state)[1] > cy:
        state, moved = moveM(state, South, flags)
        if not moved:
            fatal(state, "Couldn't move")

    while y(state)[1] < cy:
        state, moved= moveM(state, North, flags)
        if not moved:
            fatal(state, "Couldn't move")

    return state

def end_excursion(state, flags=MOVE_FLAGS):
    flags = with(flags, Movement.REWIND_EXCURSION)

    excursion = state["excursions"].pop()
    while excursion not in [None, []]:
        d = excursion.pop()
        state, moved = moveM(state, opposite(d), flags)
        if not moved:
            state = fatal(state, "Couldn't rewind excursion")

    if state["excursions"] == []:
        state["has_excursion"] = False

    return state

def move_toward(state, c, flags=MOVE_FLAGS):
    cx, cy = unpack(c)

    if x(state)[1] > cx:
        state, moved = moveM(state, West, flags)
        if moved:
            return pure(state, True)

    if x(state)[1] < cx:
        state, moved = moveM(state, East, flags)
        if moved:
            return pure(state, True)

    if y(state)[1] > cy:
        state, moved = moveM(state, South, flags)
        if moved:
            return pure(state, True)

    if y(state)[1] < cy:
        state, moved = moveM(state, North, flags)
        if moved:
            return pure(state, True)

    return pure(state, False)

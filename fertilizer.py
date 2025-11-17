from lib import *
from items import *

def fertilizable(e):
    return not contains([
        E.Dead_Pumpkin,
        None
    ], e)

def fertilize(state, over=None, n=None):
    state, e = et(state)
    if over == None or contains(over, e):
        i = 0
        while (
            fertilizable(et(state)[1])
            and not can_harvest()
            and (n == None or i < n)
            and num_items(I.Fertilizer) > 0):
            state = do_(state, [
                [useM, I.Fertilizer],
                [sense]
            ])
            i += 1
    return state

def maybe_cure(state, over=None, unsafe=False):
    e = et(state)
    if over == None or contains(over, e):
        state, infected = get_here(state, "infected")
        if infected:
            return do(state, [
                [useM, I.Weird_Substance],
                [unless, unsafe, [dos, [
                    [useM, I.Fertilizer],
                    [useM, I.Weird_Substance]
                ]]]
            ])
    return state

def cureM(state, flags=[]):
    return do(state, [
        [maybe_cure, None, Harvesting.UNSAFE in flags],
    ])

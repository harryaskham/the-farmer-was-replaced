from farmlib import *
from filler_utils import *

def filler_maze(state):
    state, d = wh(state)
    return do_(state, [
        [move_to, (d//2, d//2)],
        [maze, d, 300]
    ])

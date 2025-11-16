from farmlib import *
from filler_utils import *

def filler_maze(state):
    return dos(state, [
        [bind, [wh], [maze]]
    ])

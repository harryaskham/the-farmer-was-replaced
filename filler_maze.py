from farmlib import *
from filler_utils import *

def filler_maze(state, num_drones=None):
    return dos(state, [
        [bind, [wh], [maze]]
    ])

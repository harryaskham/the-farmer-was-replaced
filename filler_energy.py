from lib import *
from loops import *
from maze import *
from drones import *
from sunflower import *
from filler_utils import *
from compile import *

def filler_energy(state):
    return do_(state, [
        [oscillate, [Sunflower, 15, 15], [harvestM]]
    ])
    #return oscillate(state, [compile([Sunflower, 15, 15])], [compile([harvestM])])

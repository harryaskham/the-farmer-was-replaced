from farmlib import *

def filler_energy(state):
    return do_(state, [
        [oscillate, [Sunflower, 15, 15], [harvestM]]
    ])

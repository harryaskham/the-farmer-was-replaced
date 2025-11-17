from farmlib import *

COMPANION_FLAGS = [
    Spawn.SHARE,
    Spawn.BECOME,
    #Spawn.SERIAL,
    Movement.LOOP,
    #Movement.FAST,
    #To.CHILDREN,
    Movement.FAST,
    Companions.UPDATE,
    #Companions.AWAIT,
    #Companions.PLANT,
    Companions.RESERVE,
    #Growing.WATER,
    #Growing.FERTILIZE,
    #Growing.AWAIT,
    #Harvesting.CURE,
    #Harvesting.UNSAFE,
]

def filler_companions(state, flags=None):
    flags = defaults(flags, COMPANION_FLAGS)()
    f = [dos, [
        [gatherM, flags],
        [sense, flags],
        [Checker0, [cureM, flags]],
        [Companion,
            [Checker3,
                [plantM, E.Tree, flags],
                [plantM, E.Carrot, flags],
                [plantM, E.Grass, flags]
            ],
            flags
        ],
        [sense, flags]
    ]]
    return oscillate(state, f, f, flags)

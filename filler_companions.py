from farmlib import *

FLAGS = [
    Spawn.SHARE,
    Spawn.BECOME,
    #Spawn.SERIAL,
    Movement.LOOP,
    #To.CHILDREN,
    #Movement.FAST,
    Companions.UPDATE,
    #Companions.AWAIT,
    #Companions.PLANT,
    #Companions.RESERVE,
    Growing.WATER,
    Growing.FERTILIZE,
    Harvesting.CURE
]

def filler_companions(state, flags=FLAGS):
    f = [dos, [
        [try_harvest, None, flags],
        [Companion,
            [Checker3, [plantM, E.Tree, flags], [plantM, E.Carrot, flags], [plantM, E.Grass, flags]],
            flags],
        [sense, flags]
    ]]
    return oscillate(state, f, f, flags)

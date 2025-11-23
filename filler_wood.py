from farmlib import *
from filler_utils import *

def filler_wood(state):
    state, d = wh(state)
    def plant_worker(y):
        def go(state):
            return state.do([
                [move_to, (0, y)],
                [forever, [do, [
                    [try_harvest],
                    [plantM, E.Tree, [Growing.WATER]],
                    [moveM, East]
                ]]]
            ])
        return [go]

    state = do_(state, [
        [do, [
            [spawns, map(plant_worker, range(1, d))],
            plant_worker(0)
        ]]
    ])

    return state

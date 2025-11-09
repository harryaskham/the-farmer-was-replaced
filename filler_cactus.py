from lib import *
from drones import *
from cactus import *
from operators import *
from filler_utils import *

def cactus_swaps(state):
    def exists_to(state, dir):
        state, p = pos_to(state, dir)
        return pure(state, p != None)

    def noneM(state, x):
        return pure(state, x == None)

    def not_noneM(state, ma):
        return pure(state, x != None)

    def f(state, dir, op):
        return dos(state, [
            [fmap,
                [pair, dir],
                [condM, [bind, [get_to, dir, "cactus_size"], [noneM]],
                    [pure, None],
                    [lift2, [op],
                        [get_here, "cactus_size"],
                        [get_to, dir, "cactus_size"]
                    ]
                ]
            ]
        ])

    return dos(state, [
        [sense, [Sensing.DIRECTIONAL]],
        [then, [Map.from_list], [sequence, [
            [f, South, LTE],
            [f, West, LTE],
            [f, North, GT],
            [f, West, GT]
        ]]]
    ])

def filler_cactus(state):

    def maybe_swap(state, dir):
        return dos(state, [
            [condM, [popret], [pushret, True],
                [condM, [bind, [cactus_swaps], [getattr, dir]],
                    [dos, [
                        [swapM, dir],
                        [moveM, dir],
                        [pushret, True]
                    ]],
                    [pushret, False]]
            ]
        ])

    return fill_row(
        state,
        [dos, [
            [sense],
            [plant_one, E.Cactus],
            [pushret, False],
            [mapM, [maybe_swap], Dirs],
            [popret],
            [get_row]
        ]],
        [dos, [
            [bind, [popret], [merge_row]]
        ]],
        1
    )

from lib import *
from drones import *
from cactus import *
from operators import *
from filler_utils import *

def cactus_swaps(state):
    def f(state, dir, op):
        return dos(state, [
            [fmap,
                [pair, dir],
                [lift2, [op],
                    [get_here, "cactus_size"],
                    [get_to, dir, "cactus_size"]
                ]]
        ])

    return dos(state, [
        [sense, [Sensing.DIRECTIONAL]],
        [then, [Map.from_list], [sequence, [
            [f, South, lift(LTE)],
            [f, West, lift(LTE)],
            [f, North, lift(GT)],
            [f, West, lift(GT)]
        ]]]
    ])

def filler_cactus(state):

    return fill_row(
        state,
        [dos, [
            [sense],
            [plant_one, E.Cactus],
            [whileM,
                [liftA2, [lift(Or)],
                    [bind, [cactus_swaps], [getattr, West]],
                ],
                [dos, [
                    [condM, [bind, [swap_dir], [getattr, West]],
                        [dos, [
                            [swapM, West],
                            [moveM, West],
                        ]],
                        [whenM, [bind, [swap_dir], [getattr, South]],
                            [dos, [
                                [swapM, West],
                                [moveM, West],
                            ]],
                        ]
                    ],
                ]]
             ],
            [get_row]
        ]],
        [dos, [
            [bind, [popret], [merge_row]]
        ]],
        1
    )

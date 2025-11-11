from lib import *
from drones import *
from cactus import *
from operators import *
from filler_utils import *

def cactus_swaps(state):

    def dir_to_swap_required(state, dir, op):
        return dos(state, [
            [liftA2, [pairM],
                [condM, [fmap, [lift(is_none)], [get_to, dir, "cactus_size"]],
                    [pure, None],
                    [liftA2, [lift(op)],
                        [get_here, "cactus_size"],
                        [get_to, dir, "cactus_size"]
                    ]
                ],
                [pure, dir]
            ]
        ])

    return dos(state, [
        [sense, [Sensing.DIRECTIONAL]],
        [then, [Map.from_list], [sequence, [
            [dir_to_swap_required, South, LTE],
            [dir_to_swap_required, West, LTE],
            [dir_to_swap_required, North, GT],
            [dir_to_swap_required, West, GT]
        ]]]
    ])

def filler_cactus(state):

    def maybe_swap(state):
        return dos(state, [
            [then, [let, "d2s"], [cactus_swaps]],
            [let, "swap_dir", None],
            [forM, Dirs, [dos, [
                [whenM, [fmap, [is_none], [read, "swap_dir"]], [dos, [
                    [then, [let, "swap?"], [bind, [read, "d2s"], [getattr, dir]]],
                    [whenM, [read, "swap?"], [dos, [
                        [let, "swap_dir", dir]
                    ]]]
                ]]]
            ]]],
            [condM, [bind, [read, "swap_dir"], [is_none]],
                [unit],
                [dos, [
                    [swapM, dir],
                    [moveM, dir],
                    [pure, True]
                ]]
            ]
        ])

    return fill_row(
        state,
        [dos, [
            [sense],
            [plant_one, E.Cactus],
            [maybe_swap],
            [bind, [get_row], [pushret]]
        ]],
        [dos, [
            [bind, [popret], [merge_row]]
        ]]
    )

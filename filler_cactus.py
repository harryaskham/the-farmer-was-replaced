from lib import *
from drones import *
from cactus import *
from operators import *
from filler_utils import *

def assume(state):
    state, c0 = pos_to(state, South)
    state, c1 = pos_to(state, North)
    state, c2 = pos_to(state, East)
    state, c3 = pos_to(state, West)
    for c in [c0, c1, c2, c3]:
        if c != None:
            state = set_at(state, c, {"entity_type": E.Cactus})
    return state


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
    return do_(state, [
        [oscillate,
            [dos, [[plant_one, E.Cactus], [assume], [whileM, [swap_once], [nop1]]]],
            [dos, [
                [assume],
                [whileM, [swap_once], [nop1]]
                #[cond, state["y"] % 2 == 0,
                #    [swap_once, [East, West]],
                #    [swap_once, [North, South]]
                #]
            ]],
            False
        ],
        #[wait_all],
        [harvestM]
    ])

    def handle_dir(state, dir):
        return dos(state, [
            [forM, Dirs, [dos, [
                [whenM, [then, [lift(is_none)], [read, "swap_dir"]], [dos, [
                    [then, [let, "swap?"], [bind, [read, "d2s"], [getattr, dir]]],
                    [whenM, [read, "swap?"], [dos, [
                        [let, "swap_dir", dir]
                    ]]]
                ]]]
            ]]]
        ])

    def maybe_swap(state):
        return dos(state, [
            [then, [let, "d2s"], [cactus_swaps]],
            [let, "swap_dir", None],
            [mapM, [handle_dir], Dirs],
            [condM, [bind, [read, "swap_dir"], [is_none]],
                [unit],
                [dos, [
                    [bind, [read, "swap_dir"], [swapM]],
                    [bind, [read, "swap_dir"], [moveM]],
                    [pure, True]
                ]]
            ]
        ])

    def harv(state):
        return pure(state, state["i"] % 2 == 1)

    state, d = wh(state)
    state = move_to(state, (d//2, d//2))
    while True:
        for y in range(d):
            for x in range(d):
                def f(state):
                    return dos(state, [
                        [move_to, (x, y)],
                        [plant_one, E.Cactus],
                        [assume],
                        [emplace_cactus]
                    ])
                state = spawn_(state, [f], [Spawn.AWAIT])
        state = do_(state, [
            [wait_all],
            [try_harvest]
        ])
    return state

    return fill_row(
        state,
        [dos, [
            [condM, [harv],
                [try_harvest],
                [dos, [
                    [plant_one, E.Cactus],
                    [assume],
                    [sense, [Sensing.DIRECTIONAL]],
                    [emplace_cactus],
                ]]
            ],
            [get_here]
        ]],
        [merge_cell],
        [Spawn.FORK, Spawn.BECOME]
    )

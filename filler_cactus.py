from farmlib import *
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
        return do(state, [
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

    return do(state, [
        [sense, [Sensing.DIRECTIONAL]],
        [then, [Map.from_list], [sequence, [
            [dir_to_swap_required, South, LTE],
            [dir_to_swap_required, West, LTE],
            [dir_to_swap_required, North, GT],
            [dir_to_swap_required, West, GT]
        ]]]
    ])

def filler_cactus(state):
    def sel(state):
        return pure(state, (state["i"] + state["y"]) % 2 == 0)

    state = do_(state, [
        [oscillate,
            [do, [
                [plant_one, E.Cactus],
                [assume],
                [condM, [sel],
                    [whileM, [swap_once, [East, West]], [nop1]],
                    [whileM, [swap_once, [North, South]], [nop1]],
                ]
            ]],
            [do, [
                [assume],
                [condM, [sel],
                    [whileM, [swap_once, [East, West]], [nop1]],
                    [whileM, [swap_once, [North, South]], [nop1]],
                ]
            ]],
            False
        ],
        #[wait_all],
        [harvestM]
    ])
    state["i"] += 1
    return state

    def handle_dir(state, dir):
        return do(state, [
            [forM, Dirs, [do, [
                [whenM, [then, [lift(is_none)], [read, "swap_dir"]], [do, [
                    [then, [let, "swap?"], [bind, [read, "d2s"], [getattr, dir]]],
                    [whenM, [read, "swap?"], [do, [
                        [let, "swap_dir", dir]
                    ]]]
                ]]]
            ]]]
        ])

    def maybe_swap(state):
        return do(state, [
            [then, [let, "d2s"], [cactus_swaps]],
            [let, "swap_dir", None],
            [mapM, [handle_dir], Dirs],
            [condM, [bind, [read, "swap_dir"], [is_none]],
                [unit],
                [do, [
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
                    return do(state, [
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
        [do, [
            [condM, [harv],
                [try_harvest],
                [do, [
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

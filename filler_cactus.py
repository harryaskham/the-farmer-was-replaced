from lib import *
from drones import *
from cactus import *
from operators import *
from filler_utils import *

def filler_cactus(state):

    def swap_dir(state):
        def f(state, dir, op):
            return dos(state, [
                [liftA2, [pair],
                    [pure, dir],
                    [liftA2, [op],
                        [get_here, "cactus_size"],
                        [get_to, dir, "cactus_size"]
                    ]]
            ])

        return dos(state, [
            [sense, [Sensing.DIRECTIONAL]],
            [bind,
                [liftA2, [lift(cons)],
                    [f, South, lift(LTE)],
                    [bind, [f, West, lift(LTE)], [flip, cons, []]]],
                [collect]]
        ])

    return fill_row(
        state,
        [dos, [
            [sense],
            [plant_one, E.Cactus],
            [whileM,
                [liftA2, [lift(Or)],
                    [bind, [swap_dir], [getattr, South]],
                    [bind, [swap_dir], [getattr, West]],
                    #[fmap, [getattr, West], [swap_dir]],
                    #[fmap, [getattr, South], [swap_dir]],
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

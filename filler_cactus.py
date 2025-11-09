from lib import *
from drones import *
from cactus import *
from filler_utils import *

def filler_cactus(state):

    def pred(state, dir):
        return dos(state, [
            [sense, [Sensing.DIRECTIONAL]],
            [liftA2, [pair],
                [pure, dir],
                [liftA2, [lte],
                    [get_here, "cactus_size"],
                    [get_to, dir, "cactus_size"]]]
        ])

    def pred(state, dir):
        state, c = xy(state)
        state, a = get_at(state, c, "cactus_size")
        state, n = pos_to(state, dir, c)
        state, b = get_at(state, n, "cactus_size")
        return pure(state, a >= b)

    return fill_row(
        state,
        [dos, [
            [sense],
            [plant_one, E.Cactus],
            [bind, [box], [emplace_cactus]],
            [get_row]
        ]],
        [dos, [
            [bind, [popret], [merge_row]],
            [bind, [top_right], [move_to]],
            [sense],
            [start_excursion],
            [whileM, [pred, West], [dos, [
                [swapM, West],
                [moveM, West],
            ]]],
            [end_excursion]
        ]]
    )

from farmlib import *
from mains import *
from progs import *
import sim
import run_tests

def init(state):
    return dos(state, [
        [when, Size.SMALL in state["flags"], [dos, [
            [State.set_size, Size.SMALL]
        ]]],
        [when, Size.TINY in state["flags"], [dos, [
            [State.set_size, Size.TINY]
        ]]],
        [hatM, Hats.Straw_Hat],
        [move_to, [0, 0]]
    ])

def main(state=None, flags=MAIN_FLAGS):
    flags = set(flags)

    do_sim = False
    if Mode.SIMULATE in flags:
        flags.remove(Mode.SIMULATE)
        do_sim = True

    if Mode.TEST not in flags and do_sim:
        sim.run_sim(flags)

    if state == None:
        state = State.new(flags)

    def do_tests():
        if do_sim:
            sim.run_sim(flags)
        else:
            run_tests.run(state)

    if Mode.TEST in flags:
        if Testing.LOOP in flags:
            while True:
                do_tests()
        else:
            return do_tests()

    return dos(state, [
        [init],
        [when, Phase.PURGE in flags, [filler_purge]],
        [when, Phase.SCAN in flags, [dos, [
            [farmloop, do_scan, False]
        ]]],
        [forever, [dos, [
            [when, Phase.FLIPS in flags, [do_flips]],
            [when, Phase.PROGS in flags, [dos, [
                [run_progs, progs]
            ]]],
            [when, Space.FILL in flags, [forever, [dos, [
                [when, Phase.ENERGY in flags, [filler_energy]],
                [when, Phase.PUMPKIN in flags, [filler_pumpkin]],
                [when, Phase.CROPS in flags, [filler_crops]],
                [when, Phase.CARROTS in flags, [filler_crop, E.Carrot]],
                [when, Phase.CACTUS in flags, [filler_cactus]],
                [when, Phase.COMPANIONS in flags, [filler_companions]],
                [when, Phase.MAZE in flags, [filler_maze]]
            ]]]],
            [when, Phase.DINO in flags, [dos, [
                [run_progs, purges],
                [dino, [dumb, brute, search_apple]]
            ]]],
            [when, Phase.FARM in flags, [dos, [
                [bind, [cache_loop, loop], [farmloop]]
            ]]]
        ]]]
    ])

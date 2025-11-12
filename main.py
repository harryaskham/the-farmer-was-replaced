from farmlib import *
from mains import *
from progs import *
from fillers import *
import sim
import test_main
import run_tests

def init(state):
    return do_(state, [
        [State.set_size],
        [hatM, Hats.Straw_Hat],
        [move_to, (0, 0)]
    ])

def main(state=None, flags=MAIN_FLAGS):
    flags = set(flags)

    if Execution.SIMULATION not in flags:
        flags.add(Execution.NORMAL)

    if Mode.SIMULATE in flags:
        flags.remove(Mode.SIMULATE)
        flags.remove(Execution.NORMAL)
        flags.add(Execution.SIMULATION)
        sim.run_sim(flags)

    if state == None:
        state = State.new(flags)

    if Mode.TEST in flags and Execution.SIMULATION in flags:
        runner = [test_main.main, run_tests.run, False, False]
        state = do_(state, [
            runner,
            [when, Testing.LOOP in flags, [forever, runner]]
        ])

    if Mode.RUN in flags:
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
                    #[run_progs, purges],
                    [dino, [tail_follow]],
                    #[dino, [dumb, brute, search_apple]],
                ]]],
                [when, Phase.FARM in flags, [dos, [
                    [bind, [cache_loop, loop], [farmloop]]
                ]]]
            ]]]
        ])

    return unit(state)

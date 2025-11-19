from farmlib import *
from mains import *
from progs import *
from fillers import *
import sim
import test_main
import run_tests

def main(state=None, flags=MAIN_FLAGS):
    flags = set(flags)

    if Execution.SIMULATION not in flags:
        flags.add(Execution.NORMAL)

    if Mode.SIMULATE in flags:
        flags.remove(Mode.SIMULATE)
        flags.remove(Execution.NORMAL)
        flags.add(Execution.SIMULATION)
        sim.run_sim(flags)
        return state

    if state == None:
        state = State.new(flags)

    if Mode.TEST in flags and Execution.SIMULATION in flags:
        runner = [test_main.main, run_tests.run, False, False]
        state = do_(state, [
            runner,
            [when, Testing.LOOP in flags, [forever, runner]]
        ])

    if Mode.RUN in flags:
        state = do_(state, [
            [set_size],
            [hatM, Hats.Straw_Hat],
            [sense],
            [try_harvest, [E.Hedge, E.Treasure]],
            [move_to, (0, 0)],
            [when, Phase.PURGE in flags, [filler_purge]],
            [when, Phase.SCAN in flags, [farmloop, do_scan, False]],
        ])

        go = [do, [
            [when, Phase.FLIPS in flags, [do_flips]],
            [when, Phase.PROGS in flags, [run_progs, progs]],
            [when, Phase.ENERGY in flags, [filler_energy]],
            [when, Phase.PUMPKIN in flags, [filler_pumpkin]],
            [when, Phase.CROPS in flags, [filler_crops]],
            [when, Phase.CARROTS in flags, [filler_crop, E.Carrot]],
            [when, Phase.CACTUS in flags, [filler_cactus]],
            [when, Phase.COMPANIONS in flags, [filler_companions]],
            [when, Phase.MAZE in flags, [filler_maze]],
            [when, Phase.DINO in flags, [dino, [tail_follow]]],
            [when, Phase.FARM in flags, [bind, [cache_loop, loop], [farmloop]]]
        ]]

        if Mode.LOOP in flags:
            return do_(state, [[forever, go]])
        else:
            return do_(state, [go])

    return state

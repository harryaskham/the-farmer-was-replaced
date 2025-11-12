from farmlib import *
from mains import *
from progs import *
from fillers import *
import sim
import run_tests

def init(state):
    return do_(state, [
        [State.set_size],
        [hatM, Hats.Straw_Hat],
        [move_to, (0, 0)]
    ])

def main(state=None, flags=MAIN_FLAGS):
    flags = set(flags)

    if Mode.SIMULATE in flags:
        flags.remove(Mode.SIMULATE)
        sim.run_sim(flags)

    if state == None:
        state = State.new(flags)

    def do_tests(state, verbose_before=True, verbose_after=False):
        quick_print("Running Tests")
        quick_print("=============")

        has_debug = Log.DEBUG in flags

        if verbose_before:
            if not has_debug:
                state["flags"].add(Log.DEBUG)
            state = run_tests.run(state)
            if not has_debug:
                state["flags"].remove(Log.DEBUG)

        if has_debug:
            state["flags"].remove(Log.DEBUG)
        state = run_tests.run(state)
        if has_debug:
            state["flags"].add(Log.DEBUG)

        if verbose_after:
            if not has_debug:
                state["flags"].add(Log.DEBUG)
            state = run_tests.run(state)
            if not has_debug:
                state["flags"].remove(Log.DEBUG)

        quick_print("Tests Complete")
        for module_name in state["test_results"]:
            quick_print("==============")
            quick_print(module_name)
            quick_print("-----")
            for test_name in state["test_results"][module_name]:
                quick_print(test_name)
                quick_print(state["test_results"][module_name][test_name])

        return unit(state)

    if Mode.TEST in flags:
        state = do_(state, [
            [do_tests],
            [when, Testing.LOOP in flags, [forever, [do_tests]]]
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
                    [run_progs, purges],
                    [dino, [dumb, brute, search_apple]]
                ]]],
                [when, Phase.FARM in flags, [dos, [
                    [bind, [cache_loop, loop], [farmloop]]
                ]]]
            ]]]
        ])

    return unit(state)

from farmlib import *
from mains import *
from progs import *
import sim
import test

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
    
    if Mode.SIMULATE in flags:
        flags.remove(Mode.SIMULATE)
        return sim.run_sim(flags)
        
    if state == None:
        state = State.new(flags)
        
    if Mode.TEST in flags:
        return test.tests(state)
        
    return dos(state, [
        [init],
        [when, Phase.PURGE in flags, [dos, [
            [run_progs, purges]
        ]]],
        [when, Phase.SCAN in flags, [dos, [
            [farmloop, do_scan, False]
        ]]],
        [forever, [dos, [
            [when, Phase.FLIPS in flags, [do_flips]],
            [when, Phase.PROGS in flags, [dos, [
                [run_progs, progs]
            ]]],
            [when, Phase.PUMPKIN in flags, [dos, [
                [when, Space.FILL in flags, [filler_pumpkin]]
            ]]],
            [when, Phase.ENERGY in flags, [dos, [
                [when, Space.FILL in flags, [filler_energy]]
            ]]],
            [when, Phase.CROPS in flags, [dos, [
                [when, Space.FILL in flags, [filler_crops]]
            ]]],
            [when, Phase.CARROTS in flags, [dos, [
                [when, Space.FILL in flags, [filler_crop, E.Carrot]]
            ]]],
            [when, Phase.CACTUS in flags, [dos, [
                [when, Space.FILL in flags, [filler_cactus]]
            ]]],
            [when, Phase.COMPANIONS in flags, [dos, [
                [when, Space.FILL in flags, [filler_companions]]
            ]]],
            [when, Phase.MAZE in flags, [dos, [
                [cond, Space.FILL in flags,
                    [run_progs, filler_maze],
                    [dos, [
                        [try_harvest, [E.Treasure, E.Hedge]],
                        [farmloop, do_maze]
                    ]]
                ]
            ]]],
            [when, Phase.DINO in flags, [dos, [
                #[run_progs, purges],
                [dino, [dumb, brute, search_apple]]
            ]]],
            [when, Phase.FARM in flags, [dos, [
                [bind, [cache_loop, loop], [farmloop]]
            ]]]
        ]]]
    ])

if __name__ == "__main__":
    main()
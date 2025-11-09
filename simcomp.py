import sim
import flags
from lib import *

speedup = 100000000000

def ticks_per_second():
    def f():
        wait_secs(1)
    _, _, ti = time_f(f)
    return ti

tps = ticks_per_second()

def encoder(x):
    return x * tps

def decoder(x, speedup):
    return x // 1

def runtime(f, encode):
    return sim.run_sim(flags.MAIN_FLAGS, "simcomp_base", {"f": f, "encode": encode}, speedup)
    
def runtime_with_result(f, encode):
    return sim.run_sim(flags.MAIN_FLAGS, "simcomp_result", {"f": f, "encode": encode}, speedup)
    
def run(f, encode=encoder, decode=decoder):
    t = runtime(f, encode)
    t_e = runtime_with_result(f, encode)
    e = t_e - t
    r = decode(e, speedup)
    return r    
    

def tests(state):
    expect = test.mk_expect(state)

    def f():
        n = 0
        a = 3498103
        while a != 1:
            if a % 2 == 0:
                a = a / 2
            else:
                a = 3*a + 1
            n += 1
        return n

    def sim_f():
        return run(f)

    a, secs, ticks = time_f(f)
    sim_a, sim_secs, sim_ticks = time_f(sim_f)

    debug(state, ("Normal computation", "result", a, "secs", secs, "ticks", ticks))
    debug(state, ("Sim computation", "result", sim_a, "secs", sim_secs, "ticks", sim_ticks))
    expect(state, a, sim_a)

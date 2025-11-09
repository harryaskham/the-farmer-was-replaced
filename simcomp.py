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
    

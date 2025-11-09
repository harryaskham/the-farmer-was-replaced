from farmlib import *
import simcomp

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
            
def test_simcomp(f):
    def sim_f():
        return simcomp.run(f)
    
    a, secs, ticks = time_f(f)
    sim_a, sim_secs, sim_ticks = time_f(sim_f)
    
    quick_print(("Normal computation", "result", a, "secs", secs, "ticks", ticks))
    quick_print(("Sim computation", "result", sim_a, "secs", sim_secs, "ticks", sim_ticks))
    
def test_compile():
    state = State.new()
    f = compile([pure, 123])
    state, a = f(state)
    quick_print(a, 123)

def tests():
    test_simcomp(f)
    test_compile()

tests()
    
    

from farmlib import *
import simcomp
import flags

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

def assert_equal_(a, b):
    quick_print("")
    quick_print("")
    if a == b:
        quick_print(("PASS", a, "==", b))
    else:
        quick_print(("FAIL", a, "!=", b))

def assert_equal(state, a, b):
    quick_print("")
    quick_print("")
    if a == b:
        info(state, ("PASS", a, "==", b))
    else:
        info(state, ("FAIL", a, "!=", b))

def test_simcomp(f):
    def sim_f():
        return simcomp.run(f)
    
    a, secs, ticks = time_f(f)
    sim_a, sim_secs, sim_ticks = time_f(sim_f)
    
    quick_print(("Normal computation", "result", a, "secs", secs, "ticks", ticks))
    quick_print(("Sim computation", "result", sim_a, "secs", sim_secs, "ticks", sim_ticks))
    assert_equal_(a, sim_a)

def test_compile(state):
    f = compile([pure, 123])
    state, a = f(state)
    assert_equal_(a, 123)

def test_monad(state):
    def expect(a, b):
        return assert_equal(state, dos(state, [a])[1], b)

    expect([pure, 1], 1)

def tests(state):
    #test_simcomp(f)
    #test_compile(state)
    test_monad(state)

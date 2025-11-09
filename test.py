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

def assert_equal_(a, b):
    quick_print("")
    quick_print("")
    if a == b:
        quick_print(("PASS", a, "==", b))
        return True
    else:
        quick_print(("FAIL", a, "!=", b))
        return False

def assert_equal(state, a, b, msg=None):
    if msg == None:
        msg = (a, "==", b)
    if a == b:
        info(state, ("PASS", msg))
        return True
    else:
        info(state, ("FAIL", msg))
        info(state, ("Actual:", a))
        return False

def test_simcomp(state, f):
    def sim_f():
        return simcomp.run(f)
    
    a, secs, ticks = time_f(f)
    sim_a, sim_secs, sim_ticks = time_f(sim_f)
    
    quick_print(("Normal computation", "result", a, "secs", secs, "ticks", ticks))
    quick_print(("Sim computation", "result", sim_a, "secs", sim_secs, "ticks", sim_ticks))
    return assert_equal(state, a, sim_a)

def test_compile(state):
    f = compile([pure, 123])
    state, a = f(state)
    return assert_equal(state, a, 123)

def mk_expect(state):
    def expect(a, b):
        return assert_equal(state, dos(state, [a])[1], b, ("Expect:", a, "->", b))
    return expect

def tests(state):
    info(state, "Running Tests")
    #test_simcomp(state, f)
    #test_compile(state)
    monad.tests(state)

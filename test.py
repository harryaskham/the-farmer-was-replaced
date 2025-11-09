from debug import *
from monad import dos

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

def mk_expect(state):
    def expect(a, b):
        return assert_equal(state, dos(state, [a])[1], b, ("Expect:", a, "->", b))
    return expect

from compile import *
from monad import *
from operators import *

UNBOUND = "State.UNBOUND"

def Run(state, ma):
    return do(state, [ma])

def Eval(state, ma):
    return Run(state, ma).void()

def mk(a):
    ma = {
        "value": value,
        "fs": []
    }

    ma["run"] = compile([Pure, a])

def DoU(fs):
    return fs
Do = curry(DoU)

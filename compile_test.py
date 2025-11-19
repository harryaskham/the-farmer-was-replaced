from compile import *
from monad import *
from operators import *
from test import *

def run(state):
    lift_not = lift([Not])
    id_ = compile([arg, 0], 1)
    const_ = compile([arg, 0], 2)
    f0 = compile([pure, 123])
    PlusM = lift([Plus])
    Plus1 = compile([bind, [arg, 0], [PlusM, 1]], 1)
    PlusXY = compile([do, [
        [bind, [arg, 0], [let, "x"]],
        [bind, [arg, 1], [let, "y"]],
        [liftA2, [PlusM], [read, "x"], [read, "y"]]
    ]], 2)
    PlusF = defun(["a", "b"], [liftA2, [PlusM], [read, "a"], [read, "b"]])

    return do_(state, [
        [Tests, __name__],
        [Test, [lift_not, True], False],
        [Test, [id_, 1], 1],
        [Test, [const_, 5, 1], 5],
        [Test, [f0], 123],
        [Test, [pure, Plus1(state, 5)[1]], 6],
        [Test, [Plus1, 1], 2],
        [Test, [PlusM, 1, 2], 3],
        [Test, [PlusXY, 1, 2], 3],
        [Test, [PlusF, 1, 2], 3],
        [Test,
            [bind, [Lambda_, [liftA2, [PlusM], [pure, 1], [arg, 0]]], [flap, 5]],
            6]
    ])

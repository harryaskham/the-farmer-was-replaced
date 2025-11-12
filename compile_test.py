from compile import *
from monad import *
from operators import *
from test import *

def run(state):
    lift_not = lift([Not])
    id_ = compile([arg, 0], 1)
    const_ = compile([arg, 0], 2)
    f0 = compile([pure, 123])
    AddM = lift([Add])
    Add1 = compile([bind, [arg, 0], [AddM, 1]], 1)
    AddXY = compile([dos, [
        [bind, [arg, 0], [let, "x"]],
        [bind, [arg, 1], [let, "y"]],
        [liftA2, [AddM], [read, "x"], [read, "y"]]
    ]], 2)
    AddF = defun(["a", "b"], [liftA2, [AddM], [read, "a"], [read, "b"]])

    return do_(state, [
        [Tests, __name__],
        [Test, [lift_not, True], False],
        [Test, [id_, 1], 1],
        [Test, [const_, 5, 1], 5],
        [Test, [f0], 123],
        [Test, [pure, Add1(state, 5)[1]], 6],
        [Test, [Add1, 1], 2],
        [Test, [AddM, 1, 2], 3],
        [Test, [AddXY, 1, 2], 3],
        [Test, [AddF, 1, 2], 3],
        [Test,
            [bind, [Lambda_, [liftA2, [AddM], [pure, 1], [arg, 0]]], [flap, 5]],
            6]
    ])

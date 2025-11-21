from compile import *
from compile import _1
import monad
from monad import *
from operators import *
from Type import *
import State
import List

DoBlock = Type.new(
    "DoBlock",
    [Field("statements", [], list)],
    {
        "RunDo": Lambda(
            [liftA2, [lift(monad.run_do)], _1, Call(Self, "CompileDo")]
        ),
        "CompileDo": Lambda(
            [liftA2, [lift([cons])],
                [pure, monad.do],
                [fmap, [List.singleton], GetAttr(Self, "statements")]
            ])
    },
    {},
    True)
RunDo = Method("RunDo")
CompileDo = Method("CompileDo")

def DoTest(state, testF, do_block, v):
    info(state, ("DoTest do_block:", do_block))
    ma = do_block.CompileDo()
    info(state, ("DoTest compiled:", ma))
    return testF(state, ma, v)

def DoU(fs):
    return DoBlock.new(fs)
Do = curry(DoU)

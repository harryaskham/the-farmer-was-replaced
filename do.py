from compile import *
import monad
from monad import *
from operators import *
from Type import *
import List
import _

Run = Method("Run")
Compile = Method("Compile")
DoBlock = Type.new(
    "DoBlock",
    [Field("statements", [], list)],
    {
        "Run": Defun("self", "state",
            (do, (
                _.bind("do_statement", (_.lift(Compile), _.get("self"))),
                (_.lift(monad.run_do), _.get("state"), _.get("do_statement"))))
        ),
        "Compile": Defun("self",
            _.fmap(
                pipe(List.singleton, partial(cons, monad.do)),
                (_.lift(getattr), _.get("self"), "statements"))
        )
    },
    {},
    True)

def DoTest(state, testF, do_block, v):
    info(state, ("DoTest do_block:", do_block))
    ma = do_block.Compile()
    info(state, ("DoTest compiled:", ma))
    return testF(state, ma, v)

def DoU(fs):
    return DoBlock.new(fs)
Do = curry(DoU)

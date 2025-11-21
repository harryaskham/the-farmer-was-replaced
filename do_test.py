from monad import *
from operators import *
from do import *
from compile import *
from test import *
import State

def run(state):
    return state.do_([
        [Tests, __name__],
        [Test_, Do((pure, 1)).CompileDo(), [do, [[pure, 1]]]],
        [DoTest, Test, Do((pure, 1)), 1],
    ])

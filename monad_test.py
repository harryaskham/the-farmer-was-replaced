from monad import *
from operators import *
from compile import *
from test import *

def run(state):
    return do_(state, [
        [Tests, __name__],
        [Test, [pure, 1], 1],
        [Test, [pure, None], None],
        [Test, [do, [[pure, None]]], None],
        [Test, [do, [[pushret, 42], [popret]]], 42],
        [Test, [do, [[pushret, 42], [peekret]]], 42],
        [Test, [do, [[pushret, 1], [pushret, 2], [liftA2, [pairM], [popret], [popret]]]], (2, 1)]
    ])

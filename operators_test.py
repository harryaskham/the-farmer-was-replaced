from monad import *
from operators import *
from test import *

def run(state):
    return do_(state, [
        [Tests, __name__],
        [Test, [liftA2, [lift2, LT], [pure, 1], [pure, 2]], True],
        [Test, [lift2, LT, [pure, 1], [pure, 2]], True],
        [Test, [lift1, is_none, None], True],
        [Test, [fmap, [lift1, is_none], [pure, None]], True],
        [Test, [bind, [pure, True], [lift1, Not]], False],
    ])

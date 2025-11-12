from monad import *
from operators import *
from compile import *
from test import *

def run(state):
    return do_(state, [
        [Tests, __name__],
        [Test, [liftA2, [lift2, LT], [pure, 1], [pure, 2]], True],
        [Test, [lift2, LT, [pure, 1], [pure, 2]], True],
        [Test, [lift([is_none]), None], True],
        [Test, [fmap, [Add, 1], [pure, 2]], 3],
        [Test, [fmap, [is_none], [pure, None]], True],
        [Test, [bind, [pure, True], [lift1, Not]], False],
        [Test, [lift([Mod]), 8, 5], 3],
        [Test, [lift([Mod]), -3, 5], 2],
    ])

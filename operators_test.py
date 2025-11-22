from monad import *
from operators import *
from compile import *
from test import *
import _
from _ import _0, _1

def run(state):
    return state.do_([
        [Tests, __name__],
        [Test, [liftA2, [lift2, LT], [pure, 1], [pure, 2]], True],
        [Test, [lift2, LT, [pure, 1], [pure, 2]], True],
        [Test, [lift([is_none]), None], True],
        [Test, [fmap, [Plus, 1], [pure, 2]], 3],
        [Test, [fmap, [is_none], [pure, None]], True],
        [Test, [bind, [pure, True], [lift1, Not]], False],
        [Test, [lift([Mod]), 8, 5], 3],
        [Test, [lift([Mod]), -3, 5], 2],
        [Test_, partial(Plus)(1, 2), 3],
        [Test_, partial(Plus, 1)(2), 3],
        [Test_, partial(Plus, 1, 2)(), 3],
        [Test_, pipe(partial(plus, 1), partial(mul, 3))(2), 9],
        [Test, [pipeM([lift([plus]), 1], [lift([mul, 3])]), 2], 9],
        [Test, [pipeM([plusM, 1], [mulM, 3]), 2], 9],
        [Test, [LambdaM((plusM, (pure, 1), (pure, 2)))], 3],
        [Test, [LambdaM((plusM, _0, _1)), 2, 3], 5],
        [Test, [DefunM("x", "y",
                       (plusM, _.get("x"), _.get("y"))),
                       2, 3],
                5],
        [Test, [DefunM("x", "y",
                       _.bind("z", (plusM, _.get("x"), _.get("y"))),
                       _.let("w", 10),
                       (plusM, _.get("w"), _.get("z"))),
                       2, 3],
                15],
        [Test, [DefunM("x", "y",
                       _.let("shadow", DefunM("y", "x", (subM, _.get("y"), _.get("x")))),
                       (_.get("shadow"), _.get("x"), _.get("y"))),
                       2, 3],
                -1],
    ])

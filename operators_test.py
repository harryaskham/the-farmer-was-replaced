from operators import *
import test

def run(state):
    expect = test.mk_expect(state)

    expect([liftA2, [lift2, LT], [pure, 1], [pure, 2]], True)
    expect([lift2, LT, [pure, 1], [pure, 2]], True)
    expect([lift1, is_none, None], True)
    expect([fmap, [is_none], [pure, None]], True)
    expect([bind, [pure, True], [lift1, Not]], False)

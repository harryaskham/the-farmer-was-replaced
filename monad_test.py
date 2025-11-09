from monad import *
from operators import pair
import test

def run(state):
    expect = test.mk_expect(state)

    expect([pure, 1], 1)
    expect([pure, None], None)
    expect([dos, [[pushret, 42], [popret]]], 42)
    expect([dos, [[pushret, 42], [peekret]]], 42)
    expect([dos, [[pushret, 1], [pushret, 2], [liftA2, [pair], [popret], [popret]]]], (2, 1))

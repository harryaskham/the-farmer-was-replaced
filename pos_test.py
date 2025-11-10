from pos import *
import test

def run(state):
    expect = test.mk_expect(state, __name__)

    expect([xy], (0,0))
    expect([ixy], (0,0))
    expect([pos_to, North], (0, 1))
    expect([pos_to, East], (1,0))
    expect([pos_to, South], None)
    expect([pos_to, West], None)
    expect([exists_to, North], True)
    expect([exists_to, East], True)
    expect([exists_to, South], False)
    expect([exists_to, West], False)
    expect([get_here, "ground_type"], None)
    expect([get_here, "entity_type"], None)
    expect([get_at, (1,0), "entity_type"], None)
    expect([get_at, (2,0), "entity_type"], None)
    expect([get_at, None], None)
    expect([get_at, None, "entity_type"], None)

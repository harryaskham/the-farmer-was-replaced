from monad import *
from operators import *
from compile import *
from test import *
from drones import *
import State

def memory_test(x, y):
    return [do, [
        [spawn, [compile([do, [
            [set_at, (x, y), {"entity_type": E.Tree}],
        ]])]],
        [wait_all],
        [get_at, (x, y), "entity_type"]
    ]]

def run(state):
    return state.do_([
        [Tests, __name__],
        [Test, [do, [
            [spawn, [compile([pure, 1.1])]],
            [spawn, [compile([pure, 1.2])]],
            [wait_all],
            [State.get, "child_returns"],
        ]], {"1.1": 1.1, "1.2": 1.2}],
        [Test, memory_test(1, 3), E.Tree],
        [Test, memory_test(1, 4), E.Tree],
        [Test,
            [dos, [
                [spawns, [
                    [compile(memory_test(1, 5))],
                    [compile(memory_test(1, 6))],
                ]],
                [wait_all],
                [liftA2, [pairM],
                    [get_at, (1, 5), "entity_type"],
                    [get_at, (1, 6), "entity_type"]
                ]
            ]],
            (E.Tree, E.Tree)
        ]
    ])

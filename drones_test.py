from monad import *
from operators import *
from compile import *
from test import *
from drones import *
import State

def memory_test(x, y, flags):
    n = x + y / 10.0
    return [do, [
        [spawn, [compile([do, [
            [State.put, {"i": y}],
            [wait_secsM, 2],
            [get_at, (x, y), "tail_len"],
        ]])], flags],
        [set_at, (x, y), {"tail_len": n}],
        [liftA2, [pairM],
            [wait_all],
            [State.get, "i"]]
    ]]

def run(state):
    return state.do_([
        [Tests, __name__],
        [Test, [do, [
            [spawn, [compile([pure, 1.1])], [Spawn.FORK]],
            [spawn, [compile([pure, 1.2])], [Spawn.FORK]],
            [wait_all]
        ]], {"1.1": 1.1, "1.2": 1.2}],
        [Test, [wait_all], {"1.1": 1.1, "1.2": 1.2}],
        [Test,
            memory_test(1, 3, [Spawn.SHARE]),
            ({"1.1": 1.1, "1.2": 1.2, "1.3": None}, 0)],
        [Test,
            memory_test(1, 4, [Spawn.SHARE]),
            ({"1.1": 1.1, "1.2": 1.2, "1.3": None, "1.4": None}, 4)],
        [Test,
            [dos, [
                [spawn,
                    [compile(memory_test(1, 6, [Spawn.SHARE]))],
                    [Spawn.SHARE]],
                [liftA2, [pairM],
                    [wait_all],
                    [State.get, "i"]]
            ]],
            ({"1.1": 1.1, "1.2": 1.2, "1.3": None, "1.4": None,
              "1.5": ({'1.1':1.1,'1.2':1.2,'1.3':None,'1.4':None,'1.5.6':None}),
              "1.5.6": None}, 6)],
    ])

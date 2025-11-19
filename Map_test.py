from monad import *
from operators import *
from compile import *
from test import *
import Map

def run(state):
    return do_(state, [
        [Tests, __name__],
        [Test_, Map.from_list([]), {}],
        [Test_, Map.from_list([("a", 1), ("b", 2)]), {"a": 1, "b": 2}],
        [Test_, Map.from_list([("a", 1), ("a", 2)]), {"a": 2}],
        [Test_, Map.to_list({}), []],
        [Test_, Map.to_list({"a": 1, "b": 2}), [("a", 1), ("b", 2)]],
        [Test_,
            Map.bimap(partial(Plus, "x"), partial(Plus, 1), {"a": 1, "b": 2}),
            {"xa": 2, "xb": 3}],
        [Test,
            [Map.bimapM, [plusM, "x"], [plusM, 1], {"a": 1, "b": 2}],
            {"xa": 2, "xb": 3}]
    ])

if __name__ == "__main__":
    run(State.new())

from monad import *
from operators import *
from compile import *
from builtin_types import *
from test import *
from Type import Type, Field, new

def __T__(self, a, b=123, c=0):
    self["x"] = self["sum"]()

def T__sum(self):
    return self["a"] + self["b"] + self["c"]

def get_sum(self):
    return self["sum"]()

def get_x(self):
    return self["x"]

T = new(
    Type,
    "T",
    [Field("a"), Field("b", 123), Field("c", 0, int)],
    { "__init__": __T__, "sum": T__sum, "get_sum": get_sum, "get_x": get_x},
    {},
    True)

def run(state):
    return do_(state, [
        [Tests, __name__],
        [Test_, of(None), NoneType],
        [Test_, of(True), Bool],
        [Test_, of(False), Bool],
        [Test_, of(0), Int],
        [Test_, of(123), Int],
        [Test_, of(-123), Int],
        [Test_, of(123.45), Float],
        [Test_, of(-123.45), Float],
        [Test_, of(""), String],
        [Test_, of("123"), String],
        [Test_, of("-123"), String],
        [Test_, of("123.45"), String],
        [Test_, of("-123.45"), String],
        [Test_, of("hello"), String],
        [Test_, of([]), List],
        [Test_, of([1, 2, 3]), List],
        [Test_, of((1,)), Tuple],
        [Test_, of((1, 2, 3)), Tuple],
        [Test_, of({}), Dict],
        [Test_, of({"a": 1, "b": 2}), Dict],
        [Test_, of({1, 2, 3}), Set],
        [Test_, int("123"), 123],
        [Test_, int("123.45"), 123],
        [Test_, int(".45"), 0],
        [Test_, int("-123"), -123],
        [Test_, int("-123.45"), -123],
        [Test_, float("123"), 123.0],
        [Test_, float("123.45"), 123.45],
        [Test_, float(".45"), 0.45],
        [Test_, float("-123"), -123.0],
        [Test_, float("-123.45"), -123.45],
        [Test_, new(T, 1).get_x(), 124],
        [Test_, new(T, 1, 2).get_x(), 3],
        [Test_, new(T, 1, 2, 3).get_x(), 6],
        [Test_, new(T, 1, 2, 3.142).get_x(), 6],
        [Test_, new(T, 1).get_sum(), 124],
        [Test_, new(T, 1, 2).get_sum(), 3],
        [Test_, new(T, 1, 2, 3).get_sum(), 6],
        [Test_, new(T, 1, 2, 3.142).get_sum(), 6],
    ])

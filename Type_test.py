from monad import *
from operators import *
from compile import *
from builtin_types import *
import Type
import State
from test import *

def run(state):
    return do_(state, [
        [Tests, __name__],
        [Test_, Type.of(None), Type.NoneType],
        [Test_, Type.of(True), Type.Bool],
        [Test_, Type.of(False), Type.Bool],
        [Test_, Type.of(0), Type.Int],
        [Test_, Type.of(123), Type.Int],
        [Test_, Type.of(-123), Type.Int],
        [Test_, Type.of(123.45), Type.Float],
        [Test_, Type.of(-123.45), Type.Float],
        [Test_, Type.of(""), Type.String],
        [Test_, Type.of("123"), Type.String],
        [Test_, Type.of("-123"), Type.String],
        [Test_, Type.of("123.45"), Type.String],
        [Test_, Type.of("-123.45"), Type.String],
        [Test_, Type.of("hello"), Type.String],
        [Test_, Type.of([]), Type.List],
        [Test_, Type.of([1, 2, 3]), Type.List],
        [Test_, Type.of((1,)), Type.Tuple],
        [Test_, Type.of((1, 2, 3)), Type.Tuple],
        [Test_, Type.of({}), Type.Dict],
        [Test_, Type.of({"a": 1, "b": 2}), Type.Dict],
        [Test_, Type.of({1, 2, 3}), Type.Set],
        [Test_, Type.of(State.new()), State.State],
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
    ])

from monad import *
from operators import *
from compile import *
import Type
from test import *

def run(state):
    return do_(state, [
        [Tests, __name__],
        [Test_, Type.of(None), NoneType],
    ])

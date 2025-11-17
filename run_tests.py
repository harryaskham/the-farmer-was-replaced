from monad import *
from operators import *

import Type_test
import compile_test
import monad_test
import pos_test
import operators_test
import e2e_test

def run(state):
    return do_(state, [
        [Type_test.run],
        [compile_test.run],
        [monad_test.run],
        [operators_test.run],
        [pos_test.run],
        [e2e_test.run]
    ])

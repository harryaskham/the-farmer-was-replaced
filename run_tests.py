from monad import *
from operators import *

import compile_test
import monad_test
import pos_test
import operators_test
import e2e_test

def run_module(state, module):
    state["test_results"][module.__name__] = module.run(state)
    return state

def run(state):
    return mapM(state, [run_module], [
        compile_test,
        monad_test,
        #operators_test,
        #pos_test,
        #e2e_test
    ])

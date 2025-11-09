import monad_test
import pos_test
import operators_test
import e2e_test
#import simcomp
#import compile

def run(state):
    #simcomp.tests(state)
    #compile.tests(state)
    monad_test.run(state)
    pos_test.run(state)
    operators_test.run(state)
    e2e_test.run(state)

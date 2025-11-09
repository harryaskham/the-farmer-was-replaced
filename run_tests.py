import monad
import pos
import simcomp
import compile

def run(state):
    #simcomp.tests(state)
    #compile.tests(state)
    monad.tests(state)
    pos.tests(state)

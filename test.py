from debug import *
from monad import *
from operators import *

def log_return(state, v):
    state = info(state, v)
    return pure(state, v)

def assert_equal(state, a, b, msg=None):
    if msg == None:
        msg = (a, "==", b)
    if a == b:
        return log_return(state, ("PASS", msg))
    else:
        return log_return(state, ("FAIL", msg, "Actual:", a))

def Tests(state, module_name=None):
    state["test_module_name"] = module_name
    if module_name not in state["test_results"]:
        state["test_results"][module_name] = {}
    return state

def Named(state, name, test):
    return apply(state, test, name)

def Test(state, a, b, test_name=None):
  module_name = state["test_module_name"]

  if test_name == None:
    test_i = len(state["test_results"][module_name])
    test_name = module_name + "__" + str(test_i)

  state, actual = dos(state, [a])
  state, result = assert_equal(state, actual, b, ("Expect:", a, "->", b))
  state["test_results"][module_name][test_name] = result
  return state

from debug import *
from monad import *
from operators import *

def assert_equal(state, a, b, msg=None):
    if msg == None:
        msg = (a, "==", b)
    if a == b:
        info(state, ("PASS", msg))
        return True
    else:
        info(state, ("FAIL", msg))
        info(state, ("Actual:", a))
        return False

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
    test_name = "test_" + str(test_i)

  actual = dos(state, [a])
  result = assert_equal(state, actual[1], b, ("Expect:", a, "->", b))
  state["test_results"][module_name][test_name] = result
  return pure(state, result)

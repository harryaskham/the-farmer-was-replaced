from farmlib import *

def main(state, suite, verbose_before=True, verbose_after=False):
    quick_print("Running Tests")
    quick_print("=============")

    has_debug = Log.DEBUG in state["flags"]

    if verbose_before:
        if not has_debug:
            state["flags"].add(Log.DEBUG)
        state = suite(state)
        if not has_debug:
            state["flags"].remove(Log.DEBUG)

    if has_debug:
        state["flags"].remove(Log.DEBUG)
    state = suite(state)
    if has_debug:
        state["flags"].add(Log.DEBUG)

    if verbose_after:
        if not has_debug:
            state["flags"].add(Log.DEBUG)
        state = suite(state)
        if not has_debug:
            state["flags"].remove(Log.DEBUG)

    quick_print("Tests Complete")
    for module_name in state["test_results"]:
        quick_print("==============")
        quick_print(module_name)
        quick_print("-----")
        for test_name in state["test_results"][module_name]:
            quick_print(test_name)
            quick_print(state["test_results"][module_name][test_name])

    return unit(state)

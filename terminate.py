def terminate(state):
    quick_print("Terminating with state:")
    quick_print(state)
    return terminate_()
    
def terminate_(msg=None):
    quick_print("Terminating")
    if msg != None:
        quick_print("Reason:", msg)
    return TERMINATE

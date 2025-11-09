def terminate(state):
    quick_print("Terminating with state:")
    quick_print(state)
    return terminate_()
    
def terminate_():
    quick_print("Terminating")
    return TERMINATE
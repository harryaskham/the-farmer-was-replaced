from monad import *

def start_excursion(state):
    state["excursions"].append([])
    return state
    
def current_excursion(state):
    if state["excursions"] == []:
        return unit(state)
    return pure(state, state["excursions"][-1])
    
def maybe_update_excursion(state, direction):
    state, excursion = current_excursion(state)
    if excursion == None:
        return state
    excursion.append(direction)
    return state
    

    
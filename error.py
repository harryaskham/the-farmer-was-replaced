def print_error(state):
	if not has_error(state):
		return state
		
	quick_print("")
	quick_print("Error:")
	for msg in state["error"]:
		quick_print(msg)
		
	return state
	
def set_error(state, msgs):
	state["error"] = msgs
	return state
	
def clear_error(state):
	return set_error(None)
	
def has_error(state):
	return state["error"] != None

def error(state, msgs):
	state = set_error(state, msgs)
	return print_error(state)
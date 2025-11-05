from flags import *

def debug(state, msg, level=0, prefix=None):
	if level > DEBUG_LEVEL:
		return state
	if DEBUG:
		quick_print("")
		quick_print("drone #" + str(state["this_id"]))
		if prefix == None:
			quick_print(msg)
		else:
			quick_print(prefix + " " + str(msg))
	if AIR_DEBUG:
		print(msg)
	return state

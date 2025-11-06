from flags import *
from aliases import *

def debug_(msg):
	if not GLOBAL_DEBUG:
		return
	state = {
		"flags": set([Log.DEBUG]),
		"id": "_",
		"x": "_",
		"y": "_"
	}
	return debug(state, msg)
	
error_ = debug_

def log(state, msg, level=Log.DEBUG, prefix=None):
	debug_level = 0
	for l in Log.Levels:
		if l in state["flags"]:
			debug_level = max(debug_level, Log.Levels[l])
	
	if level in Log.Levels:
		level = Log.Levels[level]

	if level > debug_level:
		return state
		
	if prefix != None:
		msg = prefix + " " + str(msg)
	
	if Log.AIR in state["flags"]:
		print(msg)
		
	quick_print("")
	quick_print("drone #" + str(state["id"]) + " @" + str(state["x"]) + "," + str(state["y"]))
	quick_print(msg)

	return state

def info(state, msg, prefix=None):
	return log(state, msg, Log.INFO, prefix)
	
def debug(state, msg, unused=None, prefix=None):
	return log(state, msg, Log.DEBUG, prefix)
	
def verbose(state, msg, prefix=None):
	return log(state, msg, Log.VERBOSE, prefix)
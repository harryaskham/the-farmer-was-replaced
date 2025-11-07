from flags import *
from aliases import *
from error import *

def log(state, msg, level=Log.DEBUG, prefix=None):
	debug_level = 0
	for l in Log.Levels:
		if l in state["flags"]:
			debug_level = max(debug_level, Log.Levels[l])
	
	if level in Log.Levels:
		n_level = Log.Levels[level]
	else:
		n_level = level

	if n_level > debug_level:
		return state
		
	if prefix != None:
		msg = prefix + " " + str(msg)
	
	if Log.AIR in state["flags"]:
		print(msg)
		
	if Log.DRONE_DETAILS in state["flags"]:
		quick_print("")
		quick_print([level, state["id"], (state["x"], state["y"])])

	quick_print([level, msg])

	return state

def info(state, msg):
	return log(state, msg, Log.INFO)
	
def debug(state, msg, unused=None, prefix=None):
	return log(state, msg, Log.DEBUG, prefix)
	
def warn(state, msg):
	return log(state, msg, Log.WARN, prefix)
	
def error(state, msg, level=Log.ERROR):
	return dos(state, [
		[throw, msg],
		[log, msg, level]
	])
	
def fatal(state, msg):
	return dos(state, [
		[error, msg, Log.FATAL],
		[terminate]
	])
	
def verbose(state, msg, prefix=None):
	return log(state, msg, Log.VERBOSE, prefix)
	
def shim_state():
	flags = set(MAIN_FLAGS)
	if Log.DRONE_DETAILS in flags:
		flags.remove(Log.DRONE_DETAILS)
	state = {
		"__type__": "State",
		"flags": flags,
		"id": "_",
		"x": "_",
		"y": "_",
		"error": None
	}
	return state
	
def info_(msg):
	return info(shim_state(), msg)
	
def debug_(msg):
	return debug(shim_state(), msg)
	
def warn_(msg):
	return warn(shim_state(), msg)
	
def error_(msg):
	return error(shim_state(), msg)
	
def fatal_(msg):
	return fatal(shim_state(), msg)
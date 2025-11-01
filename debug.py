from lib import *
from flags import *

def debug(state, msg):
	if DEBUG:
		quick_print(msg)
	if AIR_DEBUG:
		print(msg)
	return state

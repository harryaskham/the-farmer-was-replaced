from lib import *

def measureM(state, key):
	d = {}
	d[key] = measure()
	return set_here(state, d)
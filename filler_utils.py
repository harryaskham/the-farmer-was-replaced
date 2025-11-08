from lib import *
from loops import *
from maze import *
from drones import *
from sunflower import *
from pumpkin import *
from cactus import *

def get_row(state):
	state, d = wh(state)
	state, [x, y] = xy(state)
	cs = []
	for x in range(d):
		state, c = at(state, (x, y))
		cs.append(c)
	return pure(state, cs)

def result_list(state, results):
	xs = []
	for child_id in results:
		xs.append(results[child_id])
	return pure(state, xs)
	
def fill_rows(state, f, handler=None, n=None):
	if n == None:
		n = state["max_drones"]
	state, d = wh(state)
	def p(y):
		return [boxloop, [0, y, d, 1], f, [0, y], False]
	for y in range(1, min(d, n)):
		state = spawnM(state, p(y))
	state, results0 = dos(state, [p(0)])
	if handler == None:
		return state
	state, results = wait_all(state)
	results[state["id"]] = results0
	return handler(state, results)

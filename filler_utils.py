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

def merge_rows(state, results):
		for result in values(results):
				for cell in results:
						state["grid"][(cell["x"], cell["y"])] = cell
		return state

def merge_row(state, r):
        i, result = r
        for cell in result:
	        state["grid"][(cell["x"], cell["y"])] = cell
	return state

def fill_row(state, f, handler=None, n=None):
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
        for i in results:
                dos(state, [
                        [pushret, (i, results[i]],
                        [handler]
                ])
        return state
	
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

def fill_rowsM(state, f, handler):
		def h(state, results):
				return dos(state, [
						[pushret, results],
						[handler]
				])
		return fill_rows(state, f, h)

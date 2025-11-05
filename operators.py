from monad import *
from trace import *

def eq(state, a, b):
	return pure(state, a == b)
	
def eqM(state, a, b):
	#state, ax = trace(state, 3, "eqM", dos(state, [a]))
	#state, bx = trace(state, 3, "eqM", dos(state, [b]))
	state, ax = dos(state, [a])
	state, bx = dos(state, [b])
	state = debug(state, [ax, bx], 3, "petals eq?")
	return eq(state, ax, bx)
	
def flipM(state, f, a, b):
	return f(state, b, a)

def forever(state, f):
	return dos(state, [
		[whileM, [pure, True], f]
	])

def pureM(state, f):
	return seq(state, [f])
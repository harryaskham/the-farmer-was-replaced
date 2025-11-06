from monad import *
from trace import *
from strings import *

def eq(state, a, b):
	return pure(state, a == b)
	
def eqM(state, a, b):
	state, ax = dos(state, [a])
	state, bx = dos(state, [b])
	are_eq = eq(state, ax, bx)
	state = debug(state, join([ax, "==", bx], " "), 3, "petals eq?")
	return eq(state, ax, bx)
	
def flipM(state, f, a, b):
	return f(state, b, a)

def forever(state, f):
	return dos(state, [
		[whileM, [pure, True], f]
	])

def pureM(state, f):
	return seq(state, [f])
	
def do_a_flipM(state):
	do_a_flip()
	return state
from monad import *

def eq(state, a, b):
	return pure(state, a == b)
	
def eqM(state, a, b):
	state, ax = dov(state, [a])
	state, bx = dov(state, [b])
	return eq(state, ax, bx)
	
def flipM(state, f, a, b):
	return f(state, b, a)

from application import *
from dict import *

def pushret(state, v):
	state["ret"].append(v)
	return state
	
def popret(state):
	v = state["ret"].pop()
	return (state, v)

def when(state, p, xs):
	if p:
		return dos(state, [xs])
	return state
	
def whenM(state, ps, xs):
	state_ = dos(state, [ps])
	state__, p = popret(state_)
	if p:
		return dos(state__, [xs])
	return state__
	
def do(state, fs):
	for xs in fs:
		state_ = aps(xs)
		state = merge(state, state_)
	return state
	
def dos(state, xss, copy=False):
	for xs in xss:
		xs = list(xs)
		xs.insert(1, state)
		state_ = aps(xs)
		if copy:
			state = merge(state, state_)
		else:
			state = state_
	return state
	
def chain(xss):
	head = list(xss[0])
	if len(xss) == 1:
		return head
	tail = chain(xss[1:])
	head.append(tail)
	return head

def run(state, xs):
	xs = list(xs)
	xs.insert(1, state)
	return (state, aps(xs))
	
def bind(state, f, g):
	state, x = run(state, f)
	g = list(g)
	g.append(x)
	return dos(state, [g])
	
def then(state, g, f):
	return bind(state, f, g)
	
def mapM(state, f, xs):
	xss = []
	for x in xs:
		xss.append([f, x])
	return dos(state, xss)
			
def runSXY(state, f):
	f = list(f)
	f.insert(1, state["y"])
	f.insert(1, state["x"])
	return dos(state, [f])

def runSXY1(state, f, otherwise):
	f = list(f)
	f.insert(1, state["y"])
	f.insert(1, state["x"])
	f.append(otherwise)
	return dos(state, [f])

def runSXY2(state, f, a, b=[]):
	f = list(f)
	f.insert(1, state["y"])
	f.insert(1, state["x"])
	f.append(a)
	f.append(b)
	return dos(state, [f])

def wrapXY(f):
	def g(state, x, y):
		return f(state)
	return g

def nop1(state):
	return state
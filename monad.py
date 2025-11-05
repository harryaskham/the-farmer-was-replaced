from application import *
from dict import *
from debug import *
from error import *

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
	out = dos(state, [ps])
	if out == None:
		return error(state, [
			"whenM condition returned None:",
			ps
		])
	if len(out) != 2:
		return error(state, [
			"whenM condition return != 2:",
			ps
		])
	state, p = out
	if p:
		return dos(state, [xs])
	return state
	
def cond(state, c, a, b):
	if c:
		return dos(state, [a])
	else:
		return dos(state, [b])

def unless(state, c, a):
	if c:
		return state
	return dos(state, [a])

def whileM(state, cf, a):
	while True:
		state, c = dov(state, [cf])
		if not c:
			break
		state = dos(state, [a])
	return state

def untilM(state, cf, a):
	while True:
		state, c = dov(state, [cf])
		if c:
			break
		state = dos(state, [a])
	return state
	
def seq(state, xss):
	state = dos(state, xss[:-1])
	state = dos(state, [
		[bind, xss[-1], [pushret]]
	])
	return pure(state, popret(state))
	
def do(state, fs):
	for xs in fs:
		state_ = aps(xs)
		state = merge(state, state_)
	return state
	
def pure(state, x):
	return {
		"__state__": state,
		"__v__": x
	}
	
def dov(state, xss):
	out = dos(state, xss, False)
	if len(out) == 1:
		return pure(state, out)
	if len(out) != 2:
		return error(state, [
			"final doV did not return value",
			xss
		])
	return out
	
ERROR = { "ERROR": "ERROR" }
	
def dos(state, xss, copy=False):
	state = debug(state, xss, 3, "dos")
	v = None
	both = False
	for xs in xss:
		state = debug(state, xs, 3, "do")
		if state["error"] != None:
			return state
			
		xs = list(xs)
		xs.insert(1, state)
		
		out = aps(xs)
		if out == None:
			state = error(state, [
				"Do-statement returned None:",
				xs
			])
			continue
		
		if "__state__" in out:
			state_ = out["__state__"]
			v = out["__v__"]
			both = True
		else:
			state_ = out
			v = None
			both = False
			
		if copy:
			state = merge(state, state_)
		else:
			state = state_
			
	if both:
		return state, v
	else:
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
		fx = list(f)
		fx.append(x)
		xss.append(fx)
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
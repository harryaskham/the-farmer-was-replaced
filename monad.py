from application import *
from dict import *
from debug import *
from error import *
from list import *

def pushret(state, v):
	state["ret"].append(v)
	return state
	
def popret(state):
	v = state["ret"].pop()
	return state, v
	
def clearret(state):
	ret = list(state["ret"])
	state["ret"] = []
	return state, ret

def identity(x):
	return x

def identityM(state, x):
	return dos(state, [x])

def constM(state, a, b):
	return dos(state, [a])

def when(state, p, xs):
	if p:
		return dos(state, [xs])
	return unit(state)
	
def whenM(state, ps, xs):
	state, p = dos(state, [ps])
	return when(state, p, xs)
	
def cond(state, c, a, b):
	if c:
		return dos(state, [a])
	else:
		return dos(state, [b])
	
def condM(state, mc, a, b):
	state, c = dos(state, [mc])
	return cond(state, c, a, b)

def unless(state, c, a):
	if c:
		return state
	return dos(state, [a])

def whileM(state, cf, a):
	while True:
		state, c = dos(state, [cf])
		if c == False:
			break
		state = do_(state, [a])
	return state

def untilM(state, cf, a):
	while True:
		state, c = dos(state, [cf])
		if c == True:
			break
		state = dos(state, [a])
	return state

def do(state, fs):
	for xs in fs:
		state_ = aps(xs)
		state = merge(state, state_)
	return state
	
def pure(state, x):
	return state, x

def liftA2(state, f, ma, mb):
	state, a = dos(state, [ma])
	state, b = dos(state, [mb])
	return apply(state, f, [a, b])

def unit(state):
	return pure(state, None)
	
def dos(state, xss):
	state = debug(state, ("dos", xss))
	
	if xss == []:
		return unit(state)
		
	v = None
	for xs in xss:
		if state["error"] != None:
			fatal(state, ("Error in do-block:", state["error"]))
			v = None
			break
				
		state = debug(state, ("do", xs))
			
		xs = list(xs)
		xs.insert(1, state)
		
		out = aps(xs)
		if out == None:
			state_, v = state, None
		elif "__type__" in out and state["__type__"] == "State":
			state_, v = out, None
		else:
			state_, v = out
			if "__type__" not in state_ or state_["__type__"] != "State":
				state = error(state, ["Malformed state returned:", state_, v])
				continue
				
		state = state_
				
	return state, v
	
def do_(state, xss):
	return dos(state, xss)[0]
	
def chain(xss):
	head = list(xss[0])
	if len(xss) == 1:
		return head
	tail = chain(xss[1:])
	head.append(tail)
	return head

def run(state, ma):
	ma = list(ma)
	ma.insert(1, state)
	return aps(ma)

def apply(state, f, args):
	fa = list(f)
	for arg in args:
		fa.append(args)
	return run(state, fa)

def bind(state, ma, f):
	state = debug(state, ("bind", ma, f))
	state, a = dos(state, [ma])
	fa = list(f)
	fa.append(a)
	return dos(state, [fa])
	
def then(state, g, f):
	return bind(state, f, g)
	
def mapM(state, f, xs):
	xss = []
	for x in xs:
		fx = list(f)
		fx.append(x)
		xss.append(fx)
	return dos(state, xss)
	
def forM(state, xs, f):
	return mapM(state, f, xs)
			
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

import Type
from application import *
from dict import *
from debug import *
from error import *
from list import *

def push_bindings(state, kvs=None):
    if kvs == None:
        kvs = {}
    state["bindings"].append(kvs)
    return state

def pop_bindings(state):
    state["bindings"].pop()
    return state

def push_binding(state, name, value):
    state["bindings"][-1][name] = value
    return state

def get_binding(state, name):
    i = len(state["bindings"])-1
    while i >= 0:
        bs = state["bindings"][i]
        if name in bs:
            return pure(state, bs[name])
        if "__call__" in bs:
            break
        i -= 1
    return fatal(state, ("Unknown binding:", name))

def pushret(state, v):
    state["ret"].append(v)
    return state

def popret(state):
    v = state["ret"].pop()
    return state, v

def peekret(state):
    v = state["ret"][-1]
    return state, v

def clearret(state):
    ret = list(state["ret"])
    state["ret"] = []
    return state, ret

def identity(x):
    return x

def identityM(state, x):
    return do(state, [x])

def constM(state, a, _):
    return do(state, [a])

def when(state, p, xs):
    if p:
        return do(state, [xs])
    return unit(state)

def whenM(state, ps, xs):
    state, p = do(state, [ps])
    return when(state, p, xs)

def cond(state, c, a, b):
    if c:
        return do(state, [a])
    else:
        return do(state, [b])

def condM(state, mc, a, b):
    state, c = do(state, [mc])
    return cond(state, c, a, b)

def unless(state, c, a):
    if c:
        return state
    return do(state, [a])

def whileM(state, cf, a):
    v = None
    while True:
        state, c = do(state, [cf])
        if c == False:
            break
        state, v = do(state, [a])
    return pure(state, v)

def untilM(state, cf, a):
    while True:
        state, c = do(state, [cf])
        if c == True:
            break
        state = do_(state, [a])
    return state

def void(state_a):
    return state_a[0]

def eval(state_a):
    return state_a[1]

def do(state, fs):
    for xs in fs:
        state_ = aps(xs)
        state = merge(state, state_)
    return state

def pure(state, x):
    return state, x

def liftA2(state, f, ma, mb):
    state, a = do(state, [ma])
    state, b = do(state, [mb])
    f = list(f)
    f.append(a)
    f.append(b)
    return do(state, [f])

def sequence(state, ms):
    vs = []
    for m in ms:
        state, v = do(state, [m])
        vs.append(v)
    return pure(state, vs)

def unit(state):
    return pure(state, None)

def x_repr(x):
    return str(x)

def do_repr(xs):
    ss = []
    for x in xs:
        ss.append(x_repr(x))
    return join(ss, " ")

def do(state, xss):
    state = verbose(state, ("dos", xss))

    if xss == []:
        return unit(state)

    v = None

    for xs in xss:
        if state["error"] != None:
            state = fatal(state, ("Error in do-block:", state["error"]))
            return unit(state)

        state = debug(state, (do, [xs]))

        xs = list(xs)
        xs.insert(1, state)

        out = aps(xs)
        if out == None:
            state_, v = state, None
        elif Type.name(out) == "State":
            state_, v = out, None
        else:
            if len(out) != 2:
                state = fatal(state, ["Malformed state,v returned:", out])
                return unit(state)
            state_, v = out
            if Type.name(state_) != "State":
                state = fatal(state, ["Malformed state returned:", state_, v])
                return unit(state)

        state = state_

    return state, v

dos = do

def do_(state, xss):
    return do(state, xss)[0]

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
        fa.append(arg)
    return run(state, fa)

def ap(state, f, arg):
    return apply(state, f, [arg])

def flap(state, arg, f):
    return apply(state, f, [arg])

def apM(state, mf, arg):
    state, f = do(state, [mf])
    return apply(state, f, args)

def flapM(state, arg, mf):
    return apM(state, mf, arg)

def bind(state, ma, f):
    state = debug(state, ("bind", ma, f))
    state, a = do(state, [ma])
    fa = list(f)
    fa.append(a)
    return do(state, [fa])

def then(state, g, f):
    return bind(state, f, g)

def mapM(state, f, xs):
    out = []
    for x in xs:
        fx = list(f)
        fx.append(x)
        state, v = do(state, [fx])
        out.append(v)
    return pure(state, out)

def forM(state, xs, f):
    return mapM(state, f, xs)

def runSXY(state, f):
    f = list(f)
    f.insert(1, state["y"])
    f.insert(1, state["x"])
    return do(state, [f])

def runSXY1(state, f, otherwise):
    f = list(f)
    f.insert(1, state["y"])
    f.insert(1, state["x"])
    f.append(otherwise)
    return do(state, [f])

def runSXY2(state, f, a, b=[]):
    f = list(f)
    f.insert(1, state["y"])
    f.insert(1, state["x"])
    f.append(a)
    f.append(b)
    return do(state, [f])

def wrapXY(f):
    def g(state, x, y):
        return f(state)
    return g

def nop1(state):
    return state

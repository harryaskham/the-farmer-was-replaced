from monad import *
from compile import *
from compile import _
from trace import *
from Type import uncurry, curry, Type, new, field

def lift1(state, f, a):
    return pure(state, f(a))

def lift2(state, f, a, b):
    return pure(state, f(a, b))

def Plus(a, b):
    return a + b

def Sub(a, b):
    return a - b

def Mul(a, b):
    return a * b

def Div(a, b):
    return a / b

def IDiv(a, b):
    return a // b

def Floor(a):
    return a // 1

def Ceil(a):
    af = Floor(a)
    if a == af:
        return af
    else:
        return af + 1

def Mod(a, b):
    return a % b

def In(x, xs):
    if xs == None:
        fatal_(("In", x, None))
    return x in xs

def Contains(xs, x):
    return In(x, xs)

def NotIn(x, xs):
    return x not in xs

def Eq(a, b):
    return a == b

def LT(a, b):
    return a < b

def LTE(a, b):
    return a <= b

def GT(a, b):
    return a > b

def GTE(a, b):
    return a >= b

def Or(a, b):
    return a or b

def And(a, b):
    return a and b

def Not(a):
    return not a
    
def Mod(a, b):
    return a % b
    
def eqM(state, a, b):
    state, ax = do(state, [a])
    state, bx = do(state, [b])
    return pure(state, eq(ax, bx))
    
def flipM(state, f, a, b):
    return f(state, b, a)

def forever(state, f):
    return do(state, [
        [whileM, [pure, True], f]
    ])

def pureM(state, f):
    return bind(state, f, [pure])
    
def do_a_flipM(state):
    do_a_flip()
    return unit(state)

def pair(a, b):
    return (a, b)

def pairM(state, a, b):
    return pure(state, (a, b))

def fst(xs):
    return xs[0]

def snd(xs):
    return xs[1]

def is_none(x):
    return x == None

def is_not_none(x):
    return not is_none(x)

def pipeU(fs):
    def p(arg):
        for f in fs:
            arg = f(arg)
        return arg
    return p
pipe = curry(pipeU)

def pipeMU(fs):
    def p(state, arg):
        for f in fs:
            state, arg = state.apply(f, [arg])
        return pure(state, arg)
    return p
pipeM = curry(pipeMU)

def maybes(xs):
    for x in xs:
        if x != None:
            return x
    return None

def partialU(f_args):
    def pU(xs):
        return applyS(f_args, xs)
    return curry(pU)
partial = curry(partialU)
partialM = lift([partial])

eq = Eq
lt = LT
lte = LTE
gt = GT
gte = GTE

plus = Plus
sub = Sub
mul = Mul
div = Div
idiv = IDiv
floor = Floor
ceil = Ceil
mod = Mod

not_ = Not
or_ = Or
and_ = And
in_ = In
not_in = NotIn
contains = Contains

ltM = lift([lt])
lteM = lift([lte])
gtM = lift([gt])
gteM = lift([gte])

plusM = lift([plus])
subM = lift([sub])
mulM = lift([mul])
divM = lift([div])
idivM = lift([idiv])
floorM = lift([floor])
ceilM = lift([ceil])
modM = lift([mod])

notM = lift([not_])
orM = lift([or_])
andM = lift([and_])
inM = lift([in_])
not_inM = lift([not_in])
containsM = lift([contains])

def GetAttr(ma, name):
    return [fmap, [partial(flip(getattr), name)], ma]

def CallU(ma_name_margs):
    ma, name, margs = ma_name_margs[0], ma_name_margs[1], ma_name_margs[2:]
    return [then, [applyM, GetAttr(ma, name)], [sequence, margs]]

Call = curry(CallU)

def LambdaU(statements):
    def p(a=_, b=_, c=_, d=_, e=_, f=_, g=_, h=_, i=_, j=_, k=_, l=_, m=_, n=_, o=_, p=_, q=_, r=_, s=_, t=_, u=_, v=_, w=_, x=_, y=_, z=_):
        args = []
        for arg in [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z]:
            if arg == _:
                break
            args.append(arg)
        state = shim_state()
        state["args"].append(args)
        state["bindings"].append({})
        state, out = state.do(statements)
        return out
    return p
Lambda = curry(LambdaU)

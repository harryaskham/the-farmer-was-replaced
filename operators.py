from monad import *
from compile import *
from trace import *

def lift1(state, f, a):
    return pure(state, f(a))

def lift2(state, f, a, b):
    return pure(state, f(a, b))

def Add(a, b):
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

eq = Eq
lt = LT
lte = LTE
gt = GT
gte = GTE

ltM = lift([lt])
lteM = lift([lte])
gtM = lift([gt])
gteM = lift([gte])

def Or(a, b):
    return a or b

def And(a, b):
    return a and b

def Not(a):
    return not a
    
def mod(state, a, b):
    return pure(state, a % b)
    
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

def fmap(state, f, ma):
    state, a = do(state, [ma])
    fa = list(f)
    fa.append(a)
    b = aps(fa)
    return pure(state, b)

def pipe(fs):
    def p(state, x):
        for f in fs:
            state, x = state.do([f, x])
        return pure(state, x)
    return p

def pipe_(fs):
    return cmp(void, pipe(fs))

def maybes(xs):
    for x in xs:
        if x != None:
            return x
    return None

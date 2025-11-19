from monad import *
from compile import *
from trace import *
from Type import uncurry, curry, Type, new, field

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

def pipeMU(state_fs):
    state, fs = state_fs[0], state_fs[1:]
    def p(state, arg):
        for f in fs:
            state, arg = state.apply(f, [arg])
        return pure(state, arg)
    return pure(state, [p])
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

eq = Eq
lt = LT
lte = LTE
gt = GT
gte = GTE

add = Add
plus = Add
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

addM = lift([add])
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

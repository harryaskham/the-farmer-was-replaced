from monad import *
from trace import *
from strings import *

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


def EQ(state, a, b):
    return pure(state, a == b)

eq = EQ

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
    
def mod(state, a, b):
    return pure(state, a % b)
    
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
    state, a = dos(state, [ma])
    fa = list(f)
    fa.append(a)
    b = aps(fa)
    return pure(state, b)

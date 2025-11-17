from application import *

def id(x):
    return x
    
def const(a, b):
    return a

def to_const3(f):
    def f_(_, _, x):
        return f(x)
    
def map(f, xs):
    ys = []
    for x in xs:
        ys.append(f(x))
    return ys

def bimap(f, g, xs):
    a, b = xs
    return (f(a), g(b))
    
def foldl(f, acc, xs):
    if xs == []:
        return acc
    return foldl(
        f, f(acc, xs[0]), xs[1:])

def foldr(f, acc, xs):
    if xs == []:
        return acc
    return f(foldr(f, acc, xs[1:]))
        
def foldl1(f, xs):
    return foldl(f, xs[0], xs[1:])
    
def foldr1(f, xs):
    return foldr(f, xs[0], xs[1:])
    
def ap(f, x):
    return f(x)

def flip(f):
    def g(x, y):
        return f(y, x)
    return g
    
def cmp(f, g):
    def fg(x):
        return f(g(x))
    return fg

precmp = flip(cmp)

def compose(fs):
    return foldr(cmp, id, fs)

def precompose(fs):
    return foldl(cmp, id, fs)
    
def cap(f, x):
    def go():
        return f(x)
    return go

def nop(_):
    return
    
def nop2(_, _):
    return
    
def nop3(_, _, _):
    return

def case(x, cases):
    x = aps(x)
    for pred, result in cases:
        pred = list(pred)
        pred.append(x)
        if aps(pred):
            return aps(result)
    fatal_(("case: no matching case", x, cases))

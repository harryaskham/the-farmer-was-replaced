import compile
import monad
import Type
import lists
from functional import map
from application import applyN

self = [compile.Arg, 0]
Self = [compile.Arg, 0]
Cls = [compile.Arg, 0]

def _(a):
    return (monad.get_, a)

wrap = monad.wrap

_0 = _(0)
_1 = _(1)
_2 = _(2)
_3 = _(3)
_4 = _(4)
_5 = _(5)
_6 = _(6)
_7 = _(7)
_8 = _(8)
_9 = _(9)
_10 = _(10)

A = _1
B = _2
C = _3
D = _4
E = _5
F = _6
G = _7
H = _8
I = _9
J = _10

def get(name):
    return (monad.get_, name)

def let(name, value):
    return (monad.let_, name, value)

def bind(name, valueM):
    return (monad.bind_, name, valueM)

def callU(name_args):
    name, args = name_args[0], name_args[1:]
    return (applyN, get(name), args)
call = Type.curry(callU)

def fmap(f, ma):
    return (monad.fmap, wrap(f), ma)

def applyMU(f_args):
    f, args = f_args[0], f_args[1:]
    return (bind, (monad.sequence, args), (monad.apply, wrap(f)))
applyM = Type.curry(applyMU)

def applyU(f_args):
    f, args = f_args[0], f_args[1:]
    return (applyN, f, args)
apply = Type.curry(applyU)

def liftU(f):
    return compile.lift(wrap(f))
lift = Type.curry(liftU)

def split_names(names_f):
    names = []
    f = []
    for i, name in lists.enumerate(names_f):
        if Type.of(name) != Type.String:
            f = names_f[i:]
            break
        names.append(names_f[i])
    return (names, f)

def withMU(names_f):
    names, f = split_names(names_f)
    return (monad.apS, f, map(get, names))
withM = Type.curry(withMU)

def withU(names_f):
    names, f = split_names(names_f)
    return (applyN, f, map(get, names))
with = Type.curry(withM)

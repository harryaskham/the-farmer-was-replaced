import compile
import monad

A = [compile.Arg, 0]
B = [compile.Arg, 1]
C = [compile.Arg, 2]
D = [compile.Arg, 3]
E = [compile.Arg, 4]
F = [compile.Arg, 5]
G = [compile.Arg, 6]
H = [compile.Arg, 7]
I = [compile.Arg, 8]
J = [compile.Arg, 9]

def get(name):
    return (compile.read, name)

def let(name, value):
    return (compile.let, name, value)

def bind(name, valueM):
    return (monad.bind, valueM, (compile.let, name))

from monad import *
import Type

_ = Type._

def push_args(state, args):
    state["args"].append(args)
    return state

def lambda(state, args, body):
    return pure(state, defun(args, body))

def Lambda(state, args, body):
    return pure(state, [defun(args, body)])

def lambda_(state, body):
    return pure(state, compile(body))

def Lambda_(state, body):
    return pure(state, [compile(body)])

def defun(args, body):
    def bind_i(state, i):
        return do(state, [
            [bind, [arg, i], [let, args[i]]]
        ])

    return compile([do, [
        [push_bindings, {"__call__": True}],
        [mapM, [bind_i], range(len(args))],
        [bind, body, [pushret]],
        [pop_bindings],
        [popret]
    ]])

def defun_(body):
    return defun([], body)

read = get_binding
let = push_binding

def pop_args(state):
    state["args"].pop()
    return state

def get_args(state):
    return pure(state, state["args"][-1])

def get_arg(state, i):
    return pure(state, state["args"][-1][i])

arg = get_arg

def compile(func, arity=None):
    def p(state, a=_, b=_, c=_, d=_, e=_, f=_, g=_, h=_, i=_, j=_, k=_):
        args = []
        for arg in [a, b, c, d, e, f, g, h, i, j, k]:
            if arg == _:
                break
            args.append(arg)
        if arity != None and len(args) > arity:
            fatal_((func), "takes", arity, "args, called with", len(args))
        return do(state, [
            [push_args, args],
            [push_bindings],
            [bind, func, [pushret]],
            [pop_bindings],
            [pop_args],
            [popret]
        ])
    return p

# lift([Plus, 1]), lift([Not])
def lift(func):
    def p(state, a=_, b=_, c=_, d=_, e=_, f=_, g=_, h=_, i=_, j=_, k=_):
        fn = list(func)
        for arg in [a, b, c, d, e, f, g, h, i, j, k]:
            if arg == _:
                break
            fn.append(arg)
        return pure(state, aps(fn))
    return p

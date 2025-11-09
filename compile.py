from monad import *
import Type

_ = Type._

def compile(func):
    def p(state, a=_, b=_, c=_, d=_, e=_, f=_, g=_, h=_, i=_, j=_, k=_):
        fn = func
        for arg in [a, b, c, d, e, f, g, h, i, j, k]:
            if arg == _:
                break
            fn.append(arg)
        return dos(state, [fn])
    return p
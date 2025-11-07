from monad import *
import Type

_ = Type.NOT_PROVIDED

def compile(f):
	def p(state, a=_, b=_, c=_, d=_, e=_, f=_, g=_, h=_, i=_, j=_, k=_):
		args = []
		for arg in [a, b, c, d, e, f, g, h, i, j, k]:
			if arg == _:
				break
			args.append(arg)
		return apply(f, args)
	return p
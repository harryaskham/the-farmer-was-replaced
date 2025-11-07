from strings import *
from monad import *
from debug import *

_ = "NOT_PROVIDED"

def mkF(handler):
	debug_(("mkF", handler))
	def fn(a=_, b=_, c=_, d=_, e=_, f=_):
		debug_(("fn", (a, b, c, d, e, f)))
		return handler([a, b, c, d, e, f])
	return fn

NO_DEFAULT = "NO_DEFAULT"

def field(name, default=NO_DEFAULT, handler=identity):
	return {
		"name": name,
		"default": default,
		"handler": handler
	}

def provided_args(args):
	xs = []
	for arg in args:
		if arg == _:
			break
		xs.append(arg)
	return xs

def method_call(self, method, args):
	f = provided_args(args)
	f.insert(0, self)
	f.insert(0, method)
	return aps(f)

def new(name, fields=[], methods={}):
	def setting_handler(self_args):
		debug_(("setting_handler", self_args))
		if len(self_args) > len(fields) + 1:
			error_(("error: more args than fields", len(args), len(fields)))
			return None

		self, args = self_args[0], self_args[1:1+len(fields)]
		for i in range(len(args)):
			arg = args[i]
			field = fields[i]
			if arg == _:
				if field["default"] == NO_DEFAULT:
					error_(("error: no default and not provided", field["name"]))
					return None
				arg = field["default"]
			self[field["name"]] = field["handler"](arg)

	if "__init__" not in methods:
		__init__ = mkF(setting_handler)
		methods["__init__"] = __init__
	
	def bound_method(self, method):
		debug_(("bound_method", self, method))
		def handler(args):
			debug_(("bound_method_handler", args))
			return method_call(self, method, args)
		return mkF(handler)

	Self = {
		"__type__": "Type",
		"__Type__": "Type",
		"__fields__": fields,
		"__methods__": methods
	}
	
	def ctor_handler(args):
		debug_(("ctor_handler", args))
		self = {
			"__type__": name,
			"__Type__": Self
		}
		for method_name in methods:
			method = methods[method_name]
			self[method_name] = bound_method(self, method)

		method_call(self, self["__init__"], args)
		return self
		
	ctor = mkF(ctor_handler)

	Self["new"] = ctor
	
	return Self
	
def name(x):
	if "__type__" in x:
		return x["__type__"]
	fatal_(("Cannot get type name of", x))
	
def of(x):
	if "__Type__" in x:
		return x["__Type__"]
	fatal_(("Cannot get Type of", x))

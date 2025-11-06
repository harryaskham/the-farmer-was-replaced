from strings import *
from monad import *
from debug import *

NOT_PROVIDED = "NOT_PROVIDED"

def mkF(handler):
	debug_(("mkF", handler))
	def fn(a=NOT_PROVIDED, b=NOT_PROVIDED, c=NOT_PROVIDED, d=NOT_PROVIDED, e=NOT_PROVIDED, f=NOT_PROVIDED):
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
			if arg == NOT_PROVIDED:
				if field["default"] == NO_DEFAULT:
					error_(("error: no default and not provided", field["name"]))
					return None
				arg = field["default"]
			self[field["name"]] = field["handler"](arg)

	if "__init__" in methods:
		__init__ = methods["__init__"]
	else:
		__init__ = mkF(setting_handler)
	
	def bound_method(self, method):
		debug_(("bound_method", self, method))
		def handler(args):
			debug_(("bound_method_handler", args))
			args = list(args)
			args.insert(0, self)
			args.insert(0, method)
			return aps(args)
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
			if method_name == "__init__":
				continue
			method = methods[method_name]
			self[method_name] = bound_method(self, method)
			
		ctor_args = [__init__, self]
		for arg in args:
			if arg == NOT_PROVIDED:
				break
			ctor_args.append(arg)
		aps(ctor_args)
		return self
		
	ctor = mkF(ctor_handler)

	Self["new"] = ctor
	
	return Self
from strings import *
from monad import *
from debug import *

_ = "NOT_PROVIDED"

def mkF(handler):
    debug_(("mkF", handler))
    def fn(a=_, b=_, c=_, d=_, e=_, f=_, g=_, h=_, i=_, j=_, k=_):
        debug_(("fn", (a, b, c, d, e, f, g, h, i, j, k)))
        return handler(provided_args([a, b, c, d, e, f, g, h, i, j, k]))
    return fn

NO_DEFAULT = "NO_DEFAULT"

def field(name, default=NO_DEFAULT, handler=identity):
    return {
        "name": name,
        "default": default,
        "handler": handler
    }

def provided_args(args):
    debug_(("provided_args", args))
    xs = []
    for arg in args:
        if arg == _:
            break
        xs.append(arg)
    return xs

def method_call(self, method, args):
    args = list(args)
    args.insert(0, self)
    return applyN(method, args)

def new(name, fields=[], methods={}, classmethods={}, dataclass=False):
    def nop_handler(self_args):
        debug_(("nop_handler", self_args))
        return None

    def setting_handler(self_args):
        debug_(("setting_handler", self_args))
        if len(self_args) > len(fields) + 1:
            fatal_(("error: more args than fields", len(args), len(fields)))

        self, args = self_args[0], self_args[1:1+len(fields)]
        for i in range(len(args)):
            arg = args[i]
            field = fields[i]
            if arg == _:
                if field["default"] == NO_DEFAULT:
                    fatal_(("error: no default and not provided", field["name"]))
                arg = field["default"]
            self[field["name"]] = field["handler"](arg)

    if "__init__" in methods:
        prev_init = methods["__init__"]

        if dataclass:
            def combined_init(self_args):
                debug_(("combined_init", self_args))
                setting_handler(self_args)
                self, args = self_args[0], self_args[1:]
                method_call(self, prev_init, args)
            __init__ = mkF(combined_init)
        else:
            __init__ = mkF(prev_init)
    elif dataclass:
        __init__ = mkF(setting_handler)
    else:
        __init__ = mkF(nop_handler)

    methods["__init__"] = __init__

    def bound_method(self, method):
        debug_(("bound_method", self, method))
        def handler(args):
            debug_(("bound_method_handler", args))
            return method_call(self, method, args)
        return mkF(handler)

    def ctor_handler(Self_args):
        Self, args = Self_args[0], Self_args[1:]
        verbose_(("ctor_handler", Self, args))
        self = {"__type__": Self}
        for method_name in methods:
            method = methods[method_name]
            self[method_name] = bound_method(self, method)
        applyN(self["__init__"], args)
        return self

    classmethods["new"] = mkF(ctor_handler)

    Self = {
        "name": name,
        "fields": fields,
        "methods": methods,
        "classmethods": classmethods,
        "dataclass": dataclass
    }
    for method_name in classmethods:
        method = classmethods[method_name]
        Self[method_name] = bound_method(Self, method)

    return Self

def __Type__(self, name, fields=[], methods={}, classmethods={}, dataclass=False):
    self["T"] = self["make"]()
    self["T"]["__type__"] = Type

def __Type__make(self):
    return new(
        self["name"],
        self["fields"],
        self["methods"],
        self["classmethods"],
        self["dataclass"])

Type = new(
    "Type",
    [
        field("name"),
        field("fields", []),
        field("methods", {}),
        field("classmethods", {}),
        field("dataclass", False)
    ],
    {
        "__init__": __Type__,
    },
    True
)

def name(x):
    return of(x)["name"]

__Builtin__ = "__Builtin__"

def Builtin(name):
    return {
        "__type__": __Builtin__,
        "name": name,
        "fields": [],
        "methods": {},
        "classmethods": {},
        "dataclass": False
    }

NoneType = Builtin("None")
String = Builtin("String")
Bool = Builtin("Bool")
Int = Builtin("Int")
Float = Builtin("Float")
List = Builtin("List")
Dict = Builtin("Dict")
Set = Builtin("Set")

NUM_CHARS = set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "+", "."])

def of(x):
    r = repr(x)
    if r == "None":
        return NoneType
    elif r == "True" or r == "False":
        return Bool
    elif r[0] == "[":
        return List
    elif r[0] == "{":
        if "__type__" in x:
            return x["__type__"]
        for c in r:
            if c == ":":
                return Dict
            elif c in [",", "}"]:
                return Set
    elif r[0] in '"' or "'":
        return String
    elif r[0] in NUM_CHARS:
        for c in r:
            if c == ".":
                return Float
        return Int

    fatal_(("Cannot get Type of", x))

def repr(x):
    return str(x)

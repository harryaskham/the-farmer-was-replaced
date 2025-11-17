from application import *
from functional import *
from debug import *
from dict import *
from builtin_types import *

_ = "NOT_PROVIDED"
NO_DEFAULT = "NO_DEFAULT"

def mkF(handler):
    debug_(("mkF", handler))
    def fn(a=_, b=_, c=_, d=_, e=_, f=_, g=_, h=_, i=_, j=_, k=_):
        debug_(("mkF fn", (a, b, c, d, e, f, g, h, i, j, k)))
        return handler(provided_args([a, b, c, d, e, f, g, h, i, j, k]))
    return fn

def identity_handler(arg):
    return arg

def field(name, default=NO_DEFAULT, handler=identity_handler):
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

def bound_method(self, method):
    debug_(("bound_method", self, method))
    def handler(args):
        debug_(("bound_method_handler", args))
        return method_call(self, method, args)
    return mkF(handler)

def mk_init(Self):
    debug_(("mk_init", Self))
    fields = Self["fields"]
    methods = Self["methods"]
    dataclass = Self["dataclass"]

    def nop_handler(self_args):
        debug_(("nop_handler", self_args))
    nop_init = mkF(nop_handler)

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
    setting_init = mkF(setting_handler)

    inits = [nop_init]
    if dataclass:
        inits.append(setting_init)
    if "__init__" in methods:
        inits.append(methods["__init__"])

    def combined_handler(self_args):
        debug_(("combined_init", self_args))
        self, args = self_args[0], self_args[1:]
        for init in inits:
            method_call(self, init, args)
    combined_init = mkF(combined_handler)

    return combined_init

def __newlist__(Self_args):
    verbose_(("__newlist__", Self_args))
    Self, args = Self_args[0], Self_args[1:]
    self = {"__type__": Self}
    for method_name, method in items(Self["methods"]):
        self[method_name] = bound_method(self, method)
    applyN(self["__init__"], args)
    return self

__new__ = mkF(__newlist__)

def Type__str__(self):
    return join(["Type<", self["name"], ">"])

def default__str__(self):
    T = of(self)
    ss = [T["name"], "({"]
    for i in range(len(T["fields"])):
        field = T["fields"][i]
        ss.append(field["name"])
        ss.append(": ")
        if field["name"] in self:
            ss.append(repr(self[field["name"]]))
        else:
            ss.append("<unset>")
        if i < len(T["fields"]) - 1:
            ss.append(", ")
    ss.append("})")
    return join(ss)

def new(name, fields=[], methods={}, classmethods={}, dataclass=False):
    fields = list(fields)
    methods = dict(methods)
    classmethods = dict(classmethods)

    Self = {
        "name": name,
        "fields": fields,
        "methods": methods,
        "classmethods": classmethods,
        "dataclass": dataclass
    }

    Self["classmethods"]["new"] = __new__

    if "__str__" not in Self["methods"]:
        Self["methods"]["__str__"] = default__str__

    Self["methods"]["__init__"] = mk_init(Self)

    for method_name, method in items(Self["classmethods"]):
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

def __Type__new(cls, name, fields=[], methods={}, classmethods={}, dataclass=False):
    return new(name, fields, methods, classmethods, dataclass)

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
    {
        "__str__": Type__str__,
    },
    True
)

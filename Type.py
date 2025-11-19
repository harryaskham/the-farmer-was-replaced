from application import *
from functional import *
from debug import *
from dict import *
from builtin_types import *

_ = "NOT_PROVIDED"
NO_DEFAULT = "NO_DEFAULT"

def uncurry(f):
    def g(xs):
        return applyN(f, xs)
    return g

def curry(uncurried):
    verbose_(("curry", uncurried))
    def curried(a=_, b=_, c=_, d=_, e=_, f=_, g=_, h=_, i=_, j=_, k=_):
        verbose_(("curry fn", (a, b, c, d, e, f, g, h, i, j, k)))
        return uncurried(provided_args([a, b, c, d, e, f, g, h, i, j, k]))
    return curried

def identity_handler(arg):
    return arg

def field(name, default=NO_DEFAULT, handler=identity_handler):
    return {
        "name": name,
        "default": default,
        "handler": handler
    }
Field = field

def provided_args(args):
    verbose_(("provided_args", args))
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
    verbose_(("bound_method", self, method))
    def handler(args):
        verbose_(("bound_method_handler", args))
        return method_call(self, method, args)
    return curry(handler)

def mk_init(Self):
    verbose_(("mk_init", Self))

    def nop_handler(self_args):
        verbose_(("nop_handler", self_args))
    nop_init = curry(nop_handler)

    def setting_handler(self_args):
        verbose_(("setting_handler", self_args))

        self, args = self_args[0], self_args[1:]
        if len(args) > len(Self["fields"]) + 1:
            fatal_(("error: more args than fields", len(args), len(Self["fields"])))

        for i in range(len(Self["fields"])):
            field = Self["fields"][i]
            arg = _
            if i < len(args):
                arg = args[i]
            if arg == _:
                if field["default"] == NO_DEFAULT:
                    fatal_(("error: no default and not provided", field["name"]))
                arg = field["default"]
            self[field["name"]] = field["handler"](arg)
    setting_init = curry(setting_handler)

    inits = [nop_init]
    if Self["dataclass"]:
        inits.append(setting_init)
    if "__init__" in Self["methods"]:
        inits.append(Self["methods"]["__init__"])

    def combined_handler(self_args):
        verbose_(("combined_init", self_args))
        self, args = self_args[0], self_args[1:]
        for init in inits:
            method_call(self, init, args)
    combined_init = curry(combined_handler)

    return combined_init

def __new__(Self_args):
    verbose_(("__new__", Self_args))
    Self, args = Self_args[0], Self_args[1:]

    self = {"__type__": Self}

    for method_name, method in items(Self["methods"]):
        self[method_name] = bound_method(self, method)

    if "__str__" not in self:
        self["__str__"] = bound_method(self, default__str__)

    init = mk_init(Self)
    self["__init__"] = bound_method(self, init)
    args = list(args)
    while len(args) < len(Self["fields"]):
        args.append(_)
    applyN(self["__init__"], args)

    return self

new = curry(__new__)

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

def __Typelist__(self_args):
    self, name, fields, methods, classmethods, dataclass = self_args

    for method_name, method in items(self["classmethods"]):
        self[method_name] = bound_method(self, method)

    if "__str__" not in self:
        self["__str__"] = bound_method(self, Type__str__)

__Type__ = curry(__Typelist__)

PreType = {
    "name": "Type",
    "fields": [
        field("name"),
        field("fields", [], list),
        field("methods", {}, dict),
        field("classmethods", {}, dict),
        field("dataclass", False)
    ],
    "methods": {
        "__init__": __Type__,
    },
    "classmethods": {
        "__str__": Type__str__,
    },
    "dataclass": True
}

Type = new(
    PreType,
    PreType["name"],
    PreType["fields"],
    PreType["methods"],
    PreType["classmethods"],
    PreType["dataclass"])
Type["__type__"] = Type

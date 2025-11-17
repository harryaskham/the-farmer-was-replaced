from terminate import *
from functional import *
from strings import *
from dict import *

Builtin = "__Builtin__"

def mk_builtin(name, ctor):
    return {
        "__type__": Builtin,
        "name": name,
        "ctor": ctor
    }

def __None__(_):
    return None

def empty(x):
    return x == [] or x == {} or x == {} or x == set()

FALSEY = set([False, None, 0, 0.0, ""])

def bool(x):
    return x not in FALSEY and not empty(x)

def ctoi(c):
    if c == "0":
        return 0
    elif c == "1":
        return 1
    elif c == "2":
        return 2
    elif c == "3":
        return 3
    elif c == "4":
        return 4
    elif c == "5":
        return 5
    elif c == "6":
        return 6
    elif c == "7":
        return 7
    elif c == "8":
        return 8
    elif c == "9":
        return 9
    terminate_(("ctoi: invalid character", c))

def parse_num(x):
    sx = str(x)
    if len(sx) == 1:
        return ctoi(sx[0])

    negate = False
    if sx[0] == "-":
        sx = sx[1:]
        negate = True

    e = 1
    int_part = 0
    float_part = None

    for i in range(len(sx)):
        c = sx[len(sx) - i - 1]
        if c == ".":
            if float_part != None:
                terminate_(("int: multiple decimal points", x))
            float_part = 1.0 * int_part
            float_part /= e
            int_part = 0
            e = 1
            continue
        int_part += ctoi(c) * e
        e *= 10

    return negate, int_part, float_part

def int(x):
    negate, n, _ = parse_num(x)
    if negate:
        n *= -1
    return n

def float(x):
    negate, int_part, float_part = parse_num(x)
    if float_part == None:
        float_part = 0.0
    n = 1.0 * int_part + float_part
    if negate:
        n *= -1.0
    return n

def tuple(x):
    if len(x) == 1:
        return (x[0],)
    if len(x) == 2:
        return (x[0], x[1])
    if len(x) == 3:
        return (x[0], x[1], x[2])
    if len(x) == 4:
        return (x[0], x[1], x[2], x[3])
    terminate_(("tuple: too many elements", x))

def function(f):
    return f

NoneType = mk_builtin("NoneType", __None__)
String = mk_builtin("String", str)
Bool = mk_builtin("Bool", bool)
Int = mk_builtin("Int", int)
Float = mk_builtin("Float", float)
List = mk_builtin("List", list)
Tuple = mk_builtin("Tuple", tuple)
Dict = mk_builtin("Dict", dict)
Set = mk_builtin("Set", set)
Function = mk_builtin("Set", function)

NUM_CHARS = set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "+", "."])

def of(x):
    r = str(x)
    if r == x:
        return String
    elif r == "None":
        return NoneType
    elif r == "True" or r == "False":
        return Bool
    elif r[0] == "[":
        return List
    elif r[0] == "(":
        return Tuple
    elif r == "{}":
        return Dict
    elif r[0] == "{":
        if "__type__" in x:
            return x["__type__"]
        for c in r:
            if c == ":":
                return Dict
            elif c in [",", "}"]:
                return Set
    elif r[0] in NUM_CHARS:
        for c in r:
            if c == ".":
                return Float
        return Int

    return Function

def is_builtin_type(t):
    return t in [NoneType, String, Bool, Int, Float, List, Tuple, Dict, Set, Function]

def is_builtin_value(t):
    return is_builtin_type(of(t))

def typed_repr(x):
    if "__str__" in x:
        return x["__str__"]()
    else:
        return str(("no __str__ method", x))

def builtin_repr(x, verbose=False):
    if verbose:
        T = of(x)
        return join([T["name"], "(", str(x), ")"])
    else:
        return str(x)

def repr(x):
    return case([of, x], [
        ([is_builtin_type],
             [builtin_repr, x]),
        ([const, True],
             [typed_repr, x])
    ])

def name(x):
    return of(x)["name"]

def eq(T, U):
    return T["name"] == U["name"]

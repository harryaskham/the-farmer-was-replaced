import flags

def floor(x):
    return x // 1

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def toggle(flags, flag):
    flags = set(flags)
    if flag in flags:
        flags.remove(flag)
    else:
        flags.add(flag)
    return flags

def without(flags, flag):
    flags = set(flags)
    if flag in flags:
        flags.remove(flag)
    return flags

def with(flags, flag):
    flags = set(flags)
    flags.add(flag)
    return flags

def default(xs, d):
    if xs == None:
        return d
    return xs

def defaults(xs, d):
    if xs == None:
        return d
    return frozenset(xs)

def frozenset(xs=None):
    if xs == None:
        xs = set()
    else:
        xs = set(xs)
    def get():
        return xs
    return get

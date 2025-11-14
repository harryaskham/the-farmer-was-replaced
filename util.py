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

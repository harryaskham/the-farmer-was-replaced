def staps(state, xs):
    xs = list(xs)
    xs.insert(1, state)
    aps(xs)

def aps(xs):
    if len(xs) == 0:
        return
    if len(xs) == 1:
        return xs[0]()
    if len(xs) == 2:
        return xs[0](xs[1])
    if len(xs) == 3:
        return xs[0](xs[1], xs[2])
    if len(xs) == 4:
        return xs[0](xs[1], xs[2], xs[3])
    if len(xs) == 5:
        return xs[0](xs[1], xs[2], xs[3], xs[4])
    if len(xs) == 6:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5])
    if len(xs) == 7:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6])
    if len(xs) == 8:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7])
    if len(xs) == 9:
        return xs[0](xs[1], xs[2], xs[3], xs[4], xs[5], xs[6], xs[7], xs[8])

def applyN(f, args):
    fa = [f]
    for arg in args:
        fa.append(arg)
    return aps(fa)

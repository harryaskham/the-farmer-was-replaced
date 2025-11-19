def singleton(x):
    return [x]

def fmap(f, xs):
    ys = []
    for x in xs:
        ys.append(f(x))
    return ys

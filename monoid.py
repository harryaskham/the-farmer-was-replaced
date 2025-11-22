def mempty():
    return []

def mappend(a, b):
    return a + b

def mconcat(xs):
    res = mempty()
    for x in xs:
        res = mappend(res, x)
    return res

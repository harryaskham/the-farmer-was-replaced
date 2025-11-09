def merge(xs, ys={}, keys=None, copy=False):
    if keys != None:
        keys = set(keys)
        
    if copy:
        xs = dict(xs)
        
    for k in ys:
        if keys == None or k in keys:
            xs[k] = ys[k]
    return xs
    
def merge_all(xss, keys=None, copy=False):
    xs = xss[0]
    for ys in xss[1:]:
        xs = merge(xs, ys, keys, copy)
    return xs
    
def copy(xs):
    return merge(xs, {}, None, True)
    
def values(xs):
    vs = []
    for k in xs:
        vs.append(xs[k])
    return vs

def getattr(xs, key, default=None):
    if key in xs:
        return xs[key]
    else:
        return default

def setattr(xs, key, value):
    xs[key] = value
    return xs

def collect(kvs):
    xs = {}
    for k, v in kvs:
        xs[k] = v
    return xs

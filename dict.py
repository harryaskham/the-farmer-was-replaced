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
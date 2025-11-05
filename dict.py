def merge(xs, ys={}):
	zs = dict(xs)
	for k in ys:
		zs[k] = ys[k]
	return zs
	
def copy(xs):
	return merge(xs, {})
def merge(xs, ys):
	if ys == None:
		return xs
	zs = dict(xs)
	for k in ys:
		zs[k] = ys[k]
	return zs
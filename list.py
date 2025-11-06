def contains(xs, x):
	for x_ in xs:
		if x == x_:
			return True
	return False

def unpack(xs):
	if len(xs) == 0:
		return None
	if len(xs) == 1:
		return xs[0]
	if len(xs) == 2:
		return xs[0], xs[1]
	if len(xs) == 3:
		return xs[0], xs[1], xs[2]
	if len(xs) == 4:
		return xs[0], xs[1], xs[2], xs[3]
		
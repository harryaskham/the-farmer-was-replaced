def all(p, xs):
	for x in xs:
		if not p(x):
			return False
	return True
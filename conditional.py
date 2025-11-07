def all(xs):
	for x in xs:
		if x:
			return False
	return True
	
def any(xs):
	for x in xs:
		if x:
			return True
	return False
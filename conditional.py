from monad import pure

def all(xs):
	for x in xs:
		if not x:
			return False
	return True
	
def any(xs):
	for x in xs:
		if x:
			return True
	return False
	
def none(xs):
	for x in xs:
		if x:
			return False
	return True

def noneM(state, xs):
	for x in xs:
		if x:
			return pure(state, False)
	return pure(state, True)
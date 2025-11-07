from lib import *
from planting import *

def Box(state, x, y, box, f=[], g=[]):
	[x0, y0, w, h] = box
	b0 = x >= x0 and y >= y0
	b1 = x < x0 + w and y < y0 + h
	if b0 and b1:
		return dos(state, [f])
	else:
		return dos(state, [g])
		
def Patch(state, x, y, x0, y0, size, f=[], g=[]):
	return Box(state, x, y, [x0, y0, x0 + size, y0 + size], f, g)

def Checker(state, x, y, f=[], g=[]):
	if (x + y) % 2 == 0:
		return dos(state, [f])
	else:
		return dos(state, [g])
		
def Checker3(state, f=[], g=[], h=[]):
	[x, y] = xy(state)
	m = (x + y) % 3
	if m == 0:
		return dos(state, [f])
	elif m == 1:
		return dos(state, [g])
	else:
		return dos(state, [h])

def Checker0(state, x, y, f):
	return Checker(state, x, y, f, [])

def Checker1(state, x, y, g):
	return Checker(state, x, y, [], g)
	
def Companion(state, otherwise=[unit]):
	def handle_companion(state, c):
		return dos(state, [
			[debug, ("companion here?", c)],
			[cond, c == None,
				otherwise,
				[plant_one, c]
			]
		])
		
	companion = get_here(state, "companion")
	return handle_companion(state, companion)
from dict import *

def mk_cell_state(x, y, kwargs=None):
	if kwargs == None:
		kwargs = {}
	state = {
		"x": x,
		"y": y,
		"entity_type": get_entity_type(),
		"ground_type": get_ground_type(),
		"companion": None,
		"companion_at": None,
		"companion_from": None
	}
	fields = {
		"infected": False,
		"water": None,
		"petals": None,
		"cactus_size": None
	}
	for k in fields:
		if k in kwargs:
			fields[k] = kwargs[k]
	return merge(state, fields)
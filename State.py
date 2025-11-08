from pos import x, y, wh
from monad import dos, when, pure
from hat import hatM
from move import move_to
from grid import mk_grid
from debug import debug_
import To
import Size
import Type

def __State__(self, flags=set()):
	debug_(("__init__", self, flags))
	self["flags"] = set(flags)
	self["id"] = 0
	self["i"] = 0
	self["x"] = get_pos_x()
	self["y"] = get_pos_y()
	self["wh"] = get_world_size()
	self["grid"] = mk_grid()
	self["ret"] = []
	self["error"] = None
	self["apple"] = None
	self["tail"] = []
	self["tail_set"] = set()
	self["tail_len"] = 0
	self["num_drones"] = 1
	self["max_drones"] = max_drones()
	self["child_handles"] = {}
	self["child_states"] = {}
	self["drone_return"] = {}
	self["treasure"] = None
	self["excursions"] = []
	debug_(("self", self))
	
def State__put(state, kvs, flags=[]):
	flags = set(flags)
	states = [state]
	if To.CHILDREN in flags:
		for child_id in state["child_states"]:
			child_state = state["child_states"][child_id]
			states.append(child_state)
	for st in states:
		for k in kvs:
			st[k] = kvs[k]
	return state
	
def State__get(self, key):
	return pure(self, self[key])

def State__fork(self, id):
	child = dict(self)
	child["id"] = id
	child["grid"] = []
	for row in self["grid"]:
		child_row = []
		for cell in row:
			child_row.append(dict(cell))
		child["grid"].append(child_row)
	child["ret"] = []
	child["child_handles"] = {}
	child["child_states"] = {}
	child["drone_return"] = {}
	child["excursions"] = []
	return child

State = Type.new(
	__name__,
	[Type.field("flags", set(), set)],
	{
		"__init__": __State__,
		"put": State__put,
		"get": State__get,
		"fork": State__fork
	})
	
new = State["new"]

def put(state, kvs, flags=[]):
	return state["put"](kvs, flags)
	
def get(state, k):
	return state["get"](k)
	
def fork(state, id):
	return state["fork"](id)
	
def set_size(state, n=Size.NORMAL):
	if n in Size.Sizes:
		n = Size.Sizes[n]
	set_world_size(n)
	return new(state["flags"])
	
def drone_id(state):
	return state["id"]
	
def loop_index(state):
	return state["i"]

from pos import x, y, wh
from monad import dos, when, pure
from hat import hatM
from move import move_to
from grid import mk_grid
from debug import debug_
import To
import Size
import Type

def __init__(self, flags=set()):
	debug_(("__init__", self, flags))
	self["flags"] = set(flags)
	self["id"] = 0
	self["i"] = 0
	self["x"] = get_pos_x()
	self["y"] = get_pos_y()
	self["wh"] = get_world_size()
	self["grid"] = mk_grid()
	self["here"] = self["grid"][self["y"]][self["x"]]
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
	debug_(("self", self))

State = Type.new(
	__name__,
	[Type.field("flags", set(), set)],
	{"__init__": __init__})
	
new = State["new"]

def put(state, kvs, flags=[]):
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
	
def set_size(state, n=Size.NORMAL):
	if n in Size.Sizes:
		n = Size.Sizes[n]
	set_world_size(n)
	return put(state, {
		"wh": get_world_size()
	}, [To.CHILDREN])
	
def drone_id(state):
	return state["id"]
	
def loop_index(state):
	return state["i"]
	
def inc_loop_index(state):
	state["i"] += 1
	return state
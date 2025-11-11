from pos import x, y, wh
from monad import dos, when, pure
from hat import hatM
from move import move_to
from debug import debug_
from locking import Lock, Unlock
import To
import Size
import Type

def __State__(self, flags=set()):
    debug_(("__init__", self, flags))

    self["id"] = num_drones()

    self["flags"] = set(flags)
    self["locks"] = {
        "__locked__": False,
        "__lockers__": set()
    }
    self["ret"] = []
    self["error"] = None
    self["args"] = []
    self["bindings"] = []
    self["stack"] = []
    self["test_module_name"] = None
    self["test_results"] = {}

    self["num_drones"] = 1
    self["max_drones"] = max_drones()
    self["child_handles"] = {}
    self["child_states"] = {}
    self["drone_return"] = {}

    self["i"] = 0
    self["x"] = get_pos_x()
    self["y"] = get_pos_y()
    self["wh"] = get_world_size()
    self["grid"] = {}
    self["excursions"] = []

    self["apple"] = None
    self["tail"] = []
    self["tail_set"] = set()
    self["tail_len"] = 0
    self["petal_counts"] = {}
    self["treasure"] = None

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

def State__fork(self):
    child = self["share"]()

    child["grid"] = {}
    for c in self["grid"]:
        child["grid"][c] = dict(self["grid"][c])

    child["petal_counts"] = {}
    for p in self["petal_counts"]:
        child["petal_counts"][p] = self["petal_counts"][p]

    return pure(self, child)

def State__share(self):
    self = Lock(self, "State__share")

    child = dict(self)
    child["id"] = num_drones() + 1

    child["ret"] = []
    child["args"] = []
    child["bindings"] = []
    child["stack"] = []
    child["test_module_name"] = None
    child["test_results"] = {}

    child["child_handles"] = {}
    child["child_states"] = {}
    child["drone_return"] = {}

    child["excursions"] = []

    child["tail"] = []
    child["tail_set"] = set()

    self = Unlock(self, "State__share")
    return child

State = Type.new(
    __name__,
    [Type.field("flags", set(), set)],
    {
        "__init__": __State__,
        "put": State__put,
        "get": State__get,
        "share": State__share,
        "fork": State__fork
    })
    
new = State["new"]

def put(state, kvs, flags=[]):
    return state["put"](kvs, flags)
    
def get(state, k):
    return state["get"](k)
    
def share(state):
    return state["share"]()

def fork(state):
    return state["fork"]()
    
def set_size(state, n=Size.NORMAL):
    if n in Size.Sizes:
        n = Size.Sizes[n]
    set_world_size(n)
    return new(state["flags"])
    
def drone_id(state):
    return state["id"]
    
def loop_index(state):
    return state["i"]

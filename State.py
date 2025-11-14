from monad import pure
from debug import debug_
from locking import Lock, Unlock
import To
import Size
import Type

def __State__(self, flags=set()):
    debug_(("__init__", self, flags))

    self["id"] = 1

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

def State__fork(self, id):
    self, child = self["share"](id)

    child["grid"] = {}
    for c in self["grid"]:
        child["grid"][c] = dict(self["grid"][c])

    child["petal_counts"] = {}
    for p in self["petal_counts"]:
        child["petal_counts"][p] = self["petal_counts"][p]

    return pure(self, child)

def State__share(self, id):
    self = Lock(self, "State__share")

    child = dict(self)
    child["id"] = id

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
    for e in self["excursions"]:
        child["excursions"].append(list(e))

    child["tail"] = []
    child["tail_set"] = set()

    child["treasure"] = None

    self = Unlock(self, "State__share")
    return pure(self, child)

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
    
def share(state, id):
    return state["share"](id)

def fork(state, id):
    return state["fork"](id)
    
def set_size(state, n=None):
    if n == None:
        for flag in state["flags"]:
            if flag in Size.Sizes:
                n = Size.Sizes[flag]
                break
        if n == None:
            return state

    if n in Size.Sizes:
        n = Size.Sizes[n]

    set_world_size(n)
    state["grid"] = {}
    state["wh"] = get_world_size()
    return state

def drone_id(state):
    return state["id"]
    
def loop_index(state):
    return state["i"]

from monad import *
from operators import *
from debug import *
from locking import *
from dict import *
from pos import *
from strings import *
import To
import Size
from Type import Type, Field, new
from flags import MAIN_FLAGS

def set_timestamps(self):
    self["start_time"] = get_time()
    self["start_ticks"] = get_tick_count()

def __State__(self, flags=MAIN_FLAGS):
    debug_(("__init__", self, flags))

    self.set_timestamps()

    self["id"] = "1"
    self["parent_id"] = None
    self["next_id"] = 1
    self["start_time"] = get_time()
    self["start_ticks"] = get_tick_count()

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

    self["child_handles"] = {}
    self["child_states"] = {}
    self["child_returns"] = {}

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
    self["maze"] = {
        "seen": set(),
        "map": set(),
        "count": 0,
        "treasure": None,
        "all_paths": {}
    }

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
    child_state = State.new(self["flags"])
    child_state["id"] = id
    for k in ["maze"]:
        child_state[k] = self[k]
    return child_state

def State__share(self, id):

    child = {}
    for k in self:
        child[k] = self[k]

    child.set_timestamps()
    child["id"] = id
    child["next_id"] = 1

    #child["ret"] = []
    #child["args"] = []
    #child["bindings"] = []
    #child["stack"] = []

    child["test_module_name"] = None
    child["test_results"] = {}

    child["child_handles"] = {}
    child["child_states"] = {}
    child["child_returns"] = {}

    child["tail"] = []
    child["tail_set"] = set()

    return child

State = new(
    Type,
    "State",
    [Field("flags", set(), set)],
    {
        "__init__": __State__,
        "put": State__put,
        "get": State__get,
        "share": State__share,
        "fork": State__fork
    },
    {},
    False)

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

def map_direction(state, dir):
    state = Lock(state, "maze_map")
    state, c = xy(state)
    state, d = pos_to(state, opposite(dir))
    state["maze"]["map"].add((c, d))
    state["maze"]["map"].add((d, c))
    state = Unlock(state, "maze_map")
    return state

def set_treasure(state, c):
    state = Lock(state, "treasure")
    state["maze"]["treasure"] = c
    state = Unlock(state, "treasure")
    return state

def with_treasure(state, f):
    state = Lock(state, "treasure")
    c = state["maze"]["treasure"]
    state, x = state.do([[f, c]])
    state = Unlock(state, "treasure")
    return pure(state, x)

def clear_treasure(state):
    return set_treasure(state, None)

def has_treasure(state):
    return with_treasure(state, lift([is_not_none]))

def incr_maze(state, limit):
    state = Lock(state, "maze_count")
    state["maze"]["count"] += 1
    cont = state["maze"]["count"] <= limit
    state = Unlock(state, "maze_count")
    return pure(state, cont)

def reset_maze(state):
    state = Lock(state, "maze_count")
    state["maze"]["count"] = 0
    state["maze"]["seen"] = set()
    state["maze"]["map"] = set()
    state["maze"]["all_paths"] = dict()
    state = Unlock(state, "maze_count")
    return state

def dump(state, level=Log.INFO):
    def log_f(state, msg):
        return log(state, msg, level, None, True)

    def dump_line(state, kv):
        return log_f(state, ['  "', kv[0], '": ', str(kv[1])].join())

    return state.do([
        [log_f, "State: {"],
        [forM, items(state), [dump_line]],
        [log_f, "}"],
    ]).void()

def get_next_id(state):
    state = Lock(state, "next_id")
    nid = [state["id"], str(state["next_id"])].join(".")
    state["next_id"] += 1
    state = Unlock(state, "next_id")
    return pure(state, nid)

def merge_state(state, other):
    state["i"] = max(state["i"], other["i"])

    for child_id, child_return in other["child_returns"].items():
        state["child_returns"][child_id] = child_return

    for c in other["maze"]["seen"]:
        state["maze"]["seen"].add(c)

    for edge in other["maze"]["map"]:
         state["maze"]["map"].add(edge)

    for from_to, path in other["maze"]["all_paths"].items():
         state["maze"]["all_paths"][from_to] = path

    state["maze"]["treasure"] = maybes([
        other["maze"]["treasure"],
        state["maze"]["treasure"]
    ])

    return state

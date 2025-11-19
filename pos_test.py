from monad import *
from operators import *
from pos import *
from test import *
from sense import *

def run(state):
    return do_(state, [
        [Tests, __name__],
        [Test, [xy], (0,0)],
        [Test, [ixy], (0,0)],
        [Test, [pos_to, North], (0, 1)],
        [Test, [pos_to, East], (1,0)],
        [Test, [pos_to, South], None],
        [Test, [pos_to, West], None],
        [Test, [exists_to, North], True],
        [Test, [exists_to, East], True],
        [Test, [exists_to, South], False],
        [Test, [exists_to, West], False],
        [Test, [do, [[sense], [get_here, "ground_type"]]], get_ground_type()],
        [Test, [do, [[sense], [get_here, "entity_type"]]], get_entity_type()],
        [Test, [get_at, (1,0), "entity_type"], None],
        [Test, [get_at, (2,0), "entity_type"], None],
        [Test, [get_at, None], None],
        [Test, [get_at, None, "entity_type"], None],
    ])

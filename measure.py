from lib import *
import State

def measureM(state, key=None, dir=None):
    if dir == None:
        m = measure()
    else:
        m = measure(dir)
        
    if dir == None:
        state, c = xy(state)
    else:
        state, c = pos_to(state, dir)
        if c == None:
            return state
        
    state, e = get_at(state, c, "entity_type")
    if key == None:
        state = do_(state, [
            [when, e == E.Cactus, [set_at, c, {"cactus_size": m}]],
            [when, e == E.Sunflower, [set_at, c, {"petals": m}]],
            [when, e == E.Apple and dir == None, [State.put, {"apple": m}]],
            [when, e == E.Hedge, [State.put, {"treasure": m}, [To.CHILDREN]]]
        ])
    else:
        state = set_at(state, c, {key: m})
    return state
from lib import *
from debug import *
from measure import *
import State

def sense_position(state):
    x = get_pos_x()
    y = get_pos_y()
    return do_(state, [
        [State.put, {
            "x": x,
            "y": y,
        }]
    ])

def sense(state, flags=[]):
    flags = set(flags)
    state = sense_position(state)
    e = get_entity_type()
    g = get_ground_type()

    state = do_(state, [
        [set_here, {
            "entity_type": e,
            "ground_type": g
        }],
    ])

    state = measureM(state)
    
    if Sensing.DIRECTIONAL in flags:
        for dir in Dirs:
            state = measureM(state, None, dir)
        
    if Companions.UPDATE not in flags:
        return state
        
    companion = get_companion()
    if companion == None:
        return verbose(state, "no companion")

    return do_(state, [
        [cond, companion == None,
            [verbose, "no companion"],
            [dos, [
                [debug, "companion/target"],
                [debug, companion],
                [bind, [at, companion[1]], [debug]],
                [set_at, companion[1], {"companion": companion[0]}, [To.CHILDREN]],
                [set_here, {"companion_at": companion[1]}, [To.CHILDREN]]
            ]]
        ]
    ])

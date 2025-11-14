from lib import *
from side_effects import *

def useM(state, item, amount=1):
    use_item(item, amount)
    if item in SIDE_EFFECTS:
        xs = SIDE_EFFECTS[item]
        return do_(state, [xs])
    return state

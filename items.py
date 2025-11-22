from lib import *
from side_effects import *

def useM(state, item, amount=1, run_side_effects=True):
    use_item(item, amount)
    if run_side_effects and item in SIDE_EFFECTS:
        xs = SIDE_EFFECTS[item]
        return do_(state, [xs])
    return state

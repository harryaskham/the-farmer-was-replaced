from farmlib import *
from test import *
import _

def run(state):
    return do_(state, [
        [Tests, __name__],
        [Test,
            [do, [
                [move_to, (0, 0)],
                [sense, [Sensing.DIRECTIONAL]],
                [liftA2, [pairM],
                    [liftA2, [pairM], [exists_to, South], [exists_to, West]],
                    [liftA2, [pairM], [exists_to, North], [exists_to, East]]
                ]
            ]],
            ((False, False), (True, True))],
    ])

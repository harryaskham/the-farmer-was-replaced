from farmlib import *
from test import *

def run(state):
    return do_(state, [
        [Tests, __name__],
        [Test,
            [dos, [
                [move_to, (0, 0)],
                [sense, [Sensing.DIRECTIONAL]],
                [liftA2, [pair],
                    [liftA2, [pair], [exists_to, South], [exists_to, West]],
                    [liftA2, [pair], [exists_to, North], [exists_to, East]]
                ]
            ]],
            ((False, False), (True, True))]
    ])

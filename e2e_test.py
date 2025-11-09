from farmlib import *
import test

def run(state):
    expect = test.mk_expect(state)

    expect(
        [dos, [
            [move_to, (0, 0)],
            [sense, [Sensing.DIRECTIONAL]],
            [liftA2, [pair],
                [liftA2, [pair], [exists_to, South], [exists_to, West]],
                [liftA2, [pair], [exists_to, North], [exists_to, East]]
            ]
        ]],
        ((False, False), (True, True)))

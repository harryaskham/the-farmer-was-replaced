from lib import *
from loops import *
from maze import *
from drones import *
from sunflower import *
from filler_utils import *

def filler_energy(state):
    def most_petals(state):
        state = Lock(state, "petal_counts")
        counts = state["petal_counts"]
        most_p = None
        total = 0
        state = info(state, ("counts", counts))
        for p in counts:
            count = counts[p]
            total += count
            if count > 0 and ((most_p == None) or (p > most_p)):
                most_p = p
        state = info(state, ("counts", counts, "total", total, "most_p", most_p))
        if total < 10:
            most_p = None
        state = Unlock(state, "petal_counts")
        return pure(state, most_p)

    def plant_tracked(state):
        state = water_to(state)
        state, planted = plant_one(state, E.Sunflower)
        if planted:
            state = sense(state)
            state, petals = get_here(state, "petals")

            state = Lock(state, "petal_counts")
            if petals not in state["petal_counts"]:
                state["petal_counts"][petals] = 0
            state["petal_counts"][petals] += 1
            state = Unlock(state, "petal_counts")
        return state

    def harvest_if_biggest(state):
        state = sense(state)
        state, petals = get_here(state, "petals")

        if petals != None:
            state = Lock(state, "petal_counts")
            state, biggest = most_petals(state)
            state = info(state, ("biggest", biggest, "here", petals, "counts", state["petal_counts"]))
            if biggest != None and petals >= biggest and can_harvest():
                state = try_harvest(state)
                state = sense(state)
                state, e = et(state)
                if e == None:
                    state["petal_counts"][petals] -= 1
            state = Unlock(state, "petal_counts")

        return state

    def cell_fn(state):
        return dos(state, [
            [harvest_if_biggest],
            [plant_tracked],
            [get_here]
        ])

    def cell_handler(state, cell):
        return merge_cell(state, cell)

    def recompute_petal_counts(state):
        for p in range(7, 16):
            state["petal_counts"][p] = 0
        for c in state["grid"]:
            cell = state["grid"][c]
            if cell["petals"] != None:
                state["petal_counts"][cell["petals"]] += 1
        return state

    def harvest_pass(state):
        for i in range(9):
            def cell_fn(state):
                return dos(state, [
                    [sense],
                    [harvest_if_biggest],
                    [get_here]
                ])
            state = fill_grid(
                state,
                [cell_fn],
                cell_handler,
                recompute_petal_counts,
                [Spawn.FORK, Spawn.BECOME]
            )
        return recompute_petal_counts(state)

    def final_handler(state):
        return do_(state, [
            [recompute_petal_counts],
            [print_grid, Log.INFO],
            [harvest_pass]
        ])

    return dos(state, [
        [forever, [dos, [
            [fill_grid,
                [cell_fn],
                cell_handler,
                final_handler,
                [Spawn.FORK, Spawn.BECOME]
             ],
            [print_grid, Log.INFO],
            [bind, [State.get, "petal_counts"], [info]],
            [bind, [State.get, "id"], [info]]
        ]]]
    ])

    state, d = wh(state)

    def sunflower_at(state, c):
        return spawn_(state, [dos, [
            [move_to, c],
            [fast_sunflower, 7, 7],
        ]])

    def boost_at(state, c):
        return spawn_(state, [dos, [
            [move_to, c],
            [forever, [boost, 10, 15, 15]]
        ]])

    def spaced(n=32, gap=1):
        cs = []
        for y in range(0, d, gap+1):
            for x in range(0, d, gap+1):
                cs.append((x, y))
                if len(cs) == n:
                    break
            if len(cs) == n:
                break
        return cs

    def sunflower_row(n=10):
        cs = []
        for x in range(n):
            cs.append([x, d-1])
        return cs

    def planter(state, y):
        return dos(state, [
            [boxloop, [0, y, d, 1], [dos, [
                [Sunflower, 7, 15]
            ]]]
        ])

    def harvester(state, y):
        state["petal_threshold"] = 15

        def decr(state):
            state["petal_threshold"] -= 1
            return state

        def reset(state):
            state["petal_threshold"] = 15
            return state

        def do_harv(state):
            state, h = get_here(state)
            petals = h["petals"]
            return pure(state, petals != None and petals >= state["petal_threshold"])

        return dos(state, [
            [boxloop, [0, y, d, 1], [dos, [
                [sense],
                [whenM, [do_harv], [dos, [
                    [try_harvest],
                    [reset]
                ]]],
                [whenM, [bind, [xy], [eq, [d-1, y]]], [decr]]
            ]]]
        ])

    return dos(state, [
        [mapM, [sunflower_at], sunflower_row()],
        [wait_all],
        [mapM, [boost_at], spaced()[1:]],
        [forever, [boost]]
    ])

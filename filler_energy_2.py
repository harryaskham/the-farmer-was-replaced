from lib import *
from loops import *
from maze import *
from drones import *
from sunflower import *
from filler_utils import *

def filler_energy_2(state):
    def most_petals(state):
        state = Lock(state, "petal_counts")
        counts = state["petal_counts"]
        most_p = None
        total = 0
        state = info(state, ("counts", counts))
        for p in counts:
            count = counts[p]
            total += count
            if count > 0 and ((most_p == None) or (p >= most_p)):
                most_p = p
        state = info(state, ("counts", counts, "total", total, "most_p", most_p))
        if total < 10:
            most_p = None
        state = Unlock(state, "petal_counts")
        return pure(state, most_p)

    def plant_tracked(state):
        state = do_(state, [
            [Sunflower, 15, 15]
        ])
        planted = True
        #state, planted = plant_one(state, E.Sunflower)
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
                state["petal_counts"][petals] -= 1
            state = Unlock(state, "petal_counts")

        return state

    def cell_fn(state):
        return do(state, [
            [harvest_if_biggest],
            [plant_tracked],
            [get_here]
        ])

    def recompute_petal_counts(state):
        for p in range(7, 16):
            state["petal_counts"][p] = 0
        for c in state["grid"]:
            cell = state["grid"][c]
            if cell["petals"] != None:
                state["petal_counts"][cell["petals"]] += 1
        return state

    def harvest_pass(state):
        def cell_fn(state):
            return do(state, [
                [try_harvest],
                [get_here]
            ])
        return fill_grid(
            state,
            [cell_fn],
            merge_cell,
            None,
            [Spawn.SHARE, Spawn.BECOME])

    def final_handler(state):
        return do_(state, [
            [recompute_petal_counts],
            [print_grid, Log.INFO],
            [move_to, (0, 0)],
            [harvest_pass]
        ])

    return do(state, [
        [forever, [do, [
            [fill_grid,
                [cell_fn],
                merge_cell,
                final_handler,
                [Spawn.FORK, Spawn.BECOME]
             ],
            [print_grid, Log.INFO],
            [bind, [State.get, "petal_counts"], [info]],
            [bind, [State.get, "id"], [info]]
        ]]]
    ])

from dict import *
from aliases import *
import flags

all_items = {}
for i in Items:
	all_items[i] = 10**10
	
def run_sim(main_flags=flags.MAIN_FLAGS, name="simulation", globals={}, speedup=64, seed=random() * 100000 // 1, unlocks=Unlocks, items=all_items):
	main_flags = set(main_flags)
	if Mode.SIMULATE in main_flags:
		main_flags.remove(Mode.SIMULATE)
	globals["MAIN_FLAGS"] = main_flags

		
	t = simulate(
		name,
		unlocks,
		items,
		globals,
		seed,
		speedup)
		
	quick_print("sim complete in " + str(t) + " seconds")
	
	return t
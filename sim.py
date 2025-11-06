from dict import *
from aliases import *

seed = random() * 100000 // 1
speedup = 65535

all_unlocks = Unlocks

all_items = {}
for i in Items:
	all_items[i] = 10**4
	
all_globals = {}

def run_sim(main_flags=[]):
	main_flags = set(main_flags)
	if Mode.SIMULATE in main_flags:
		main_flags.remove(Mode.SIMULATE)
		
	globals = {
		"MAIN_FLAGS": main_flags
	}
	t = simulate(
		"simulation",
		all_unlocks,
		all_items,
		globals,
		seed,
		speedup)
	quick_print("sim complete in " + str(t) + " seconds")
	return t
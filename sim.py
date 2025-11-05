from dict import *

seed = 42
speedup = 64

all_unlocks = Unlocks

all_items = {}
for i in Items:
	all_items[i] = 10**10
	
all_globals = {}
	
t = simulate(
	"simulation",
	all_unlocks,
	all_items,
	all_globals,
	seed,
	speedup)
	
quick_print("sim complete in " + str(t) + " seconds")
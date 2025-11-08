import sim
import flags

def f():
	def g(a, b):
		return a + b
	return g(3, 7)

def runtime(f, encode):
	return sim.run_sim(flags.MAIN_FLAGS, "simcomp_base", {"f": f, "encode": encode})
	
def runtime_with_result(f, encode):
	return sim.run_sim(flags.MAIN_FLAGS, "simcomp_result", {"f": f, "encode": encode})
	
def run(f, encode=identity, decode=identity):
	t = runtime(f, encode)
	t_e = runtime_with_result(f, encode)
	e = t_e - t
	r = decode(e)
	return r	
	

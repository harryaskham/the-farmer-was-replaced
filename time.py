def wait_secs(secs):
	t = get_time()
	while get_time() < t + secs:
		pass

def wait_secsM(state, secs):
	if secs > 0:
		wait_secs(secs)
	return state

def wait_ticks(ticks):
	for _ in range(ticks):
		pass
		
def time_f(f):
	t = get_time()
	ti = get_tick_count()
	r = f()
	t1 = get_time()
	ti1 = get_tick_count()
	return (r, t1-t, ti1-ti)
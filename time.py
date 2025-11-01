def wait_secs(secs):
	t = get_time()
	while get_time() < t + secs:
		pass

def wait_ticks(ticks):
	for _ in range(ticks):
		pass
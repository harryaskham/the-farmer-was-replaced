from lib import *

def flood(state, start, tail, tail_len):
	d = wh(state)
	seen = set()
	accessible = set()
	tail_set = set(tail)
	q = [(start, tail, tail_set)]
	while q != []:
		st = q[-1]
		q = q[:-1]
		state = debug(state, ("search state", st))
		(p, tail, tail_set) = st
		(px, py) = p
		
		accessible.add(p)

		if p in tail_set:
			continue
		if p in seen:
			continue
		seen.add(p)
		
		if len(seen) == d * d:
			return state, seen

		ns = neighbors_dict(state, px, py)
		for dir in ns:
			[nx, ny] = ns[dir]
			n_tup = (nx, ny)
			if n_tup in seen:
				continue
			
			next_tail = list(tail)
			next_tail_set = set(tail_set)
			next_tail.append(p)
			next_tail_set.add(p)
			while len(next_tail) > tail_len:
				if next_tail[0] in next_tail_set:
					next_tail_set.remove(next_tail[0])
				next_tail = next_tail[1:]
					
			if n_tup in next_tail_set:
				continue

			next_st = ((nx, ny), next_tail, next_tail_set)
			q.append(next_st)
			state = verbose(state, ("next state", next_st))
			
		state = verbose(state, ("q len", len(q)))
			
	return state, seen

def poor_accessible(state, c, start, tail, tail_set, tail_len):
	return path_to(state, c, False, start, tail, tail_set, tail_len)
		

def path_to(state, c, check=True, start=None, tail=None, tail_set=None, tail_len=None):
	state = debug(state, ("path_to", "at", xy(state), "apple", state["apple"], "c", c, "check", check, "tail", tail, "tlen", tail_len))
	state, d = wh(state)
	[tx, ty] = c
	c_tup = (tx, ty)
	
	def h(c):
		[cx, cy] = c
		return abs(tx - cx) + abs(ty - cy)
	
	seen = set()
	if start == None:
		start = xy_tup(state)
	if tail == None:
		tail = state["tail"]
	if tail_set == None:
		tail_set = state["tail_set"]
	if tail_len == None:
		tail_len = state["tail_len"]
	q = [(start, tail, tail_set, [])]
	while q != []:
		st = q[0]
		q = q[1:]

		(p, tail, tail_set, path) = st
		(px, py) = p
		
		state = debug(state, ("search at", p))
		state = verbose(state, ("search state", st))
		
		if p == c_tup:
			#state, accessible = flood(state, p, tail, tail_len + 1)
			#state = debug(state, ["found path leaving accessible", len(accessible), "of", d * d, "wanting", d * d - (tail_len + 1), "at", p, "tail", tail], 2, "search")
			if check:
				good = True
				for target in [(0,0), (d-1, d-1)]:
					state, p2c = poor_accessible(state, target, p, tail, tail_set, tail_len+1)
					if p2c == None:
						good = False
						state = debug(state, ("no path to", target, "from", p))
						break
					state = debug(state, ("found path to", target, "from", p, p2c))
				if not good:
					continue
					
			state = debug(state, ("found path to target", c, "from", start, path))
			return state, path
			#if len(accessible) == d * d:
			#	return state, path
			#else:
			#	continue
		
		if p in seen:
			continue
		seen.add(p)

		if p in tail_set:
			continue

		ns = neighbors_dict(state, px, py)
		all_dirs = set([North, South, East, West])
		dirs = []
		if tx < px:
			dirs.append(West)
			all_dirs.remove(West)
		if tx > px:
			dirs.append(East)
			all_dirs.remove(East)
		if ty < py:
			dirs.append(South)
			all_dirs.remove(South)
		if ty > py:
			dirs.append(North)
			all_dirs.remove(North)
		for dir in all_dirs:
			dirs.append(dir)
			
		for dir in dirs:
			if dir not in ns:
				continue
			[nx, ny] = ns[dir]
			n_tup = (nx, ny)
			if n_tup in seen:
				continue

						
			next_tail = list(tail)
			next_tail_set = set(tail_set)
			next_tail.append(p)
			next_tail_set.add(p)
			while len(next_tail) > tail_len:
				if next_tail[0] in next_tail_set:
					next_tail_set.remove(next_tail[0])
				next_tail = next_tail[1:]
					
			if n_tup in next_tail_set:
				continue
				
			next_path = list(path)
			next_path.append(dir)
			
			#if p == state["apple"] and len(next_path) < tail_len:
			#	continue
			
			next_st = ((nx, ny), next_tail, next_tail_set, next_path)
			q.append(next_st)
			state = verbose(state, ("next state", next_st))
			
		state = verbose(state, ("q len", len(q)))
			
	return state, None
	
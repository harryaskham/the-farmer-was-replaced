def moveM(state, d):
	if not move(d):
		return state	
	if d == North:
		state["y"] += 1
	elif d == South:
		state["y"] -= 1
	if d == East:
		state["x"] += 1
	elif d == West:
		state["x"] -= 1
	return state
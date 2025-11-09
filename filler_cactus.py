from lib import *
from drones import *
from cactus import *
from filler_utils import *


def filler_cactus(state):
	return fill_rows(
				state,
				[dos, [
						[plant_one, E.Cactus],
						[get_row]
				]],
				[bind, [popret], [merge_row]]
		)

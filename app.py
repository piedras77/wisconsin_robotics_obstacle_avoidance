# assume you receive an n^2 matrix

# creation of the histogram
# let Vehicle Center Point (x, y) = (0, 0)
# distance in meters
# The ZED Mini camera can perceive depth between 15 cm (0.5 feet) and 15 meters 
# width of robot: 1.2
# POD: polar obstacle density
import histogram
import grid

import math


g = grid.Grid(15, 15)
h = histogram.Histogram(72, g, 4)

# determines the min size of a wide valley, rather than min valley
# TODO: obtain better number for s_max
# Borensteing suggest s_max = 18 i.e. 90 degrees
# larger s_max the furthest robot stays from obstacle
s_max = 18

# TODO: determine threshold, find valley narrow, wide size
# note that threshold only afects width of valley, but not valley itself
threshold = 900000000

#TODO: get max speed from robot's specs
# maximum speed in meters per second
max_speed = 1.5

# returns distance (in sectors) from sector parameter to target
# returns 0 if sector parameter contains target
def get_target_distance(valley, target):
	if target < valley[0]:
		return valley[0] - target
	if target > valley[1]:
		return target - valley[1]

	return 0

# number of consecutive sectors where POD is below threshold
def is_wide_valley(valley):
	if 1 + valley[1] - valley[0] > s_max:
		return True

	return False

# represent a valley as an ordered pair as in (start sector, end sector)
# iterate through sector array to add valleys to new candidate valleys list
# from candidate valleys choose the one that is closest to target_sector
# valleys of width of one sector are valid since they can only come from smoothing function of adjacent areas. 
def select_valley(target_sector):
	best_valley = [-100, -100]
	best_distance = 80
	current_valley = [-1, -1]
	for i in range(len(h.sectors)):
		if h.sectors[i] <= threshold and current_valley[0] == -1:
			current_valley[0] = i

		if h.sectors[i] > threshold and current_valley[0] is not -1:

			current_valley[1] = i
			current_distance = get_target_distance(current_valley, target_sector)
			if  current_distance < best_distance:
				best_distance = current_distance
				best_valley = current_valley
			
			current_valley = [-1, -1]

	if current_valley[0] is not -1:
		current_valley[1] = 71
		current_distance = get_target_distance(current_valley, target_sector)
		if  current_distance < best_distance:
			best_valley = current_valley

	return best_valley


# target_sector received from global planning
def get_navigation_angle(target_sector):
	# first determine target valley
	target_valley = select_valley(target_sector)
	# from selected valley, determine target sector
	if get_target_distance(target_valley, target_sector):
		return target_sector * 5
	elif is_wide_valley(target_valley):
		nearest_sector = target_valley[1] if target_sector > target_valley[1] else target_valley[0]
		border_sector = target_valley[1] - s_max if target_sector > target_valley[1] else target_valley[0] + s_max
		return ((nearest_sector + border_sector) / 2) * 5
	else:
		return ((target_valley[1] + target_valley[0]) / 2) * 5

def get_max_speed():
	# high POD ahead implies an obstacle ahead
	# TODO: empirixally determine density_constant for correct speed reduction
	density_constant = 999999999
	density = min(density_constant, h.sectors[len(h.sectors) / 4])
	# Reduces speed in anticipation of steering maneuver
	speed = max_speed * (1 - density / density_constant)
	# Reduces speed according to actual steering angle degree per second
	# TODO: implement velocity change according to steering rate

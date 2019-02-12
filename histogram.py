import math
import matplotlib.pyplot as plt
from point import Point

class Histogram():

	threshold = 0
	sectors = [0]

	def __init__(self, sector_numbers, grid, threshold):
		self.threshold = threshold
		self.sectors = [0] * sector_numbers
		# set robots center to 0
		self.robot_center = Point(7, 7)
		# angle size of each sector
		self.alpha = 360 / sector_numbers
		self.populate_sectors(grid)
		pass

	def populate_sectors(self, grid):
		min = 1000
		max = -1
		for row in range(grid.rowSize - 1):
			for col in range(grid.colSize - 1):
				k = int(self.get_beta(grid.grid[row][col]) / self.alpha)
				self.sectors[k] += self.get_magnitude(grid.grid[row][col], grid.rowSize)

		for i in range(len(self.sectors)):
			self.sector_smoothing(i)


	# TODO: 
	# assumes sector_number is valid, integer >= 0
	def sector_smoothing(self, sector_number):
		# section 1, section two
		l = 5
		sector_counter = 1
		index = sector_number - l
		constant = 1
		while index < 0:
			index += 1
			constant += 1

		while index < sector_number:
			self.sectors[index] = (constant * self.sectors[index])
			constant += 1
			index += 1
			sector_counter += 1

		self.sectors[index] += ((l - 1) * self.sectors[index])
		while index < len(self.sectors) and index >= sector_number - l:
			self.sectors[index] = (constant * self.sectors[index])
			constant -= 1
			index -= 1
			sector_counter += 1

		self.sectors[sector_number] /= sector_counter

	def plot_histogram(self):
		plt.hist(self.sectors)
		plt.show()

	def get_magnitude(self, point, grid_size):
		# define constants a, b, s.t. a-b(d_max) = 0
		# assuming that robot is at center of vision grid
		d_max = math.sqrt(2) * (grid_size - 1) / 2
		b = 1 # TODO: find empirical value of b
		a = b  * d_max
		return math.pow(point.certainty, 2) * (a - b * point.distance)

	# gives angle relative to robot's center
	def get_beta(self, point):
		delta_y = self.robot_center.row - point.row
		result =  math.degrees(math.atan2(delta_y, point.col - self.robot_center.col))
		if delta_y < 0:
			result += 360

		return result







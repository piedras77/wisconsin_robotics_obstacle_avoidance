import math
import matplotlib.pyplot as plt

#TODO: UPDATE IT FOR LIDAR INPUT
# do magnitude 
class Histogram():
	sectors = [0]
	# Degrees the lidar can make measurements for
	LIDAR_VISION = 275

	def __init__(self, sector_count, threshold, vision_angle, data):
		self.threshold = threshold
		self.sectors = [0] * sector_count
		self.data = data
		self.alpha = 360 / sector_count
		self.vision_angle = vision_angle
		self.populate_sectors()

	# Angles of histogram go from 0-360 starting at the 
	# right hand side and moving counter clockwise
	# readings of lidar are from -138 to 138
	def populate_sectors(self):
		# LIDAR has 275 degrees of horizontal aperture
		# ranges list starts from rightmost angle to left most
		# lidar gives angular distance between measurements of 0.75 degrees
		# we want sectors starting from right hand side
		# each sector is 4, degrees, thus, we have 4 readings per sector
		# We only use the 180 degrees in front of the robot
		# i.e. skip the first 47 degrees  and ignore the last 47 degrees

		# number of measurements we need to skip from the start and the end
		trim_measurements = int(math.ceil(((self.LIDAR_VISION - self.vision_angle)/2.0)/math.degrees(self.data.angle_increment)))
		start = trim_measurements + 1
		end = len(self.data.ranges) - trim_measurements
		readings_per_sector = math.ceil(self.alpha / 0.75)
		sector_num = 0
		data_count = 0
		for i in range(start, end):
			# print(self.get_magnitude(self.data.ranges[i]))
			self.sectors[sector_num] += self.get_magnitude(self.data.ranges[i])
			data_count += 1
			if data_count >= readings_per_sector:
				sector_num += 1
				data_count = 0

		old_sectors = self.sectors[:]
		for i in range(len(self.sectors)):
			self.sector_smoothing(i, old_sectors)

		self.old_sectors = old_sectors

	def sector_smoothing(self, sector_number, old_sectors):
		l = 5
		start = sector_number - l 
		end = sector_number + l + 1
		start = 0 if start < 0 else start
		end = len(old_sectors) - 1 if end >= len(old_sectors) else end
		num = 0
		for i in range(start, end):
			constant = abs((sector_number - l) - i) + 1
			constant_2 = abs((sector_number + l) - i) + 1
			constant = min(constant, constant_2)
			num += constant * old_sectors[sector_number]

		# self.sectors[sector_number] = num / (2 * l + 1)
		self.sectors[sector_number] = num / (end - start)

	def plot_histogram(self):
		angles = [i for i in range(3, 180, self.alpha)]
		plt.plot(angles, self.sectors[0: 59])
		plt.show()

	# let the magnitude range from 0 - 1
	# the close a measurement is the greatest its magnitude
	def get_magnitude(self, distance):
		# We want a = b (self.data.range_max * self.data.range_max)
		a = 1.0
		b = a / (self.data.range_max) #  * self.data.range_max)
		return a - b * distance #* distance
	
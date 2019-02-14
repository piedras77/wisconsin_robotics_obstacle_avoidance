from point import Point

class Grid():

	def __init__(self, rowSize, colSize):
		self.rowSize = rowSize
		self.colSize = colSize
		self.grid = [[Point(j, i, 0, 0) for i in range(colSize)] for j in range(rowSize)]
		self.sample_grid()
		pass

	def get_cell(self, row, col):
		return self.grid[row][col]

	def update_values():
		pass

	def get_grid(self):
		return self.grid

	def sample_grid(self):
		for row in range(self.rowSize - 9):
			self.grid[row][3] = Point(row, 3, 90, 5)
			self.grid[row][4] = Point(row, 4, 90, 5)
			self.grid[row][5] = Point(row, 5, 90, 5)


			self.grid[row][9] = Point(row, 9, 90, 5)
			self.grid[row][10] = Point(row, 10, 90, 5)
			self.grid[row][11] = Point(row, 11, 90, 5)


		


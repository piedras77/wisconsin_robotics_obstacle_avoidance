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
			self.grid[row][5] = Point(row, 5, 90, 5)
			self.grid[row][6] = Point(row, 6, 90, 5)
			self.grid[row][7] = Point(row, 7, 90, 5)
			self.grid[row][8] = Point(row, 8, 90, 5)

		


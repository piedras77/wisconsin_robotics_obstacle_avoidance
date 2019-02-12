class Point():
	row = col = certainty = distance = 0

	def __init__(self, row, col, certainty = 0, distance = 0):
		self.row = row
		self.col = col
		self.certainty = certainty
		self.distance = distance

	def get_row():
		return row

	def get_col():
		return col

	def get_certainty():
		return certainty

	def set_row(self, row):
		self.row = row

	def set_col(self, col):
		self.col = col

	def set_certainty(self, certainty):
		self.certainty = certainty

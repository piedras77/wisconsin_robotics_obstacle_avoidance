# assume you receive an n^2 matrix

# creation of the histogram
# let Vehicle Center Point (x, y) = (0, 0)
# distance in meters
# The ZED Mini camera can perceive depth between 15 cm (0.5 feet) and 15 meters 
# width of robot: 1.2
import histogram
import grid

import math


# histogram, needs k sectors, needs a density per sector
g = grid.Grid(15, 15)
h = histogram.Histogram(72, g, 4)

def get_magnitude(certainty, distance, max):
    distance_max = math.sqrt(2) * (max - 1) / 2
    # a - b*distance_max  = 0, choose a or b



# alpha = 5, thus there are 360/5 = 72 sections
# thus, each sector k, corresponds to an angle p, such that p = k*alpha, k = 0, 1, 2, ...

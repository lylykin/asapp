
import svg.path
from sys import exit
from svg.path import parse_path

class Path: 
    points: list[(float, float)]

    def __init__(self):
        self.points = []

    def append(self, point):
        self.points.append(point)


# use the svg.path library to parse the path string
# and convert it to a list of points
# this function will take a path string and return a list of points
# the points will be in the form of a tuple (x, y)
# Quality describes the number of points to be generated for a given path
def convert_path_from_dstring(path_def, quality=5) -> Path:
    path = parse_path(path_def)
    res = Path()
    for l in range(quality+1):
        rel_point = path.point(l / quality)
        res.append((rel_point.real, rel_point.imag))
    return res

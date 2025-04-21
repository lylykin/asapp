
import svg.path
from sys import exit
from svg.path import parse_path





class Path: 
    points: list[(float, float)]

    def __init__(self):
        self.points = []

    def append(self, point):
        self.points.append(point)



def convert_path_from_dstring(path_def, quality=5) -> Path:
    path = parse_path(path_def)
    res = Path()
    for l in range(quality):
        rel_point = path.point(l / quality)
        res.append((rel_point.real, rel_point.imag))
    return res

        
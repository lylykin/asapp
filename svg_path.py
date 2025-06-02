
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


def raw_svg_path(path_def: Path) -> Path:
    try:
        path = parse_path(path_def)
    except Exception as e:
        print(f"Error parsing path: {e}")
        exit(1)

    raw = []
    for l in range(30):  # 30 is an arbitrary number to get enough points
        rel_point = path.point(l / 30)
        raw.append((rel_point.real, rel_point.imag))

    p = Path()
    p.points = raw 
    return p 


# source: https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
def distance_to_line(pa1, pa2, pb):
    """
    Calculate the distance from point pb to the line defined by points pa1 and pa2.
    """
    if pa1 == pa2:
        return ((pb[0] - pa1[0]) ** 2 + (pb[1] - pa1[1]) ** 2) ** 0.5

    # Line equation coefficients
    A = pa2[1] - pa1[1] # y2 - y1
    B = pa1[0] - pa2[0] # x1 - x2
    C = pa2[0] * pa1[1] - pa1[0] * pa2[1] # x2*y1 - x1*y2

    # Distance from point to line
    # return |Ax + By + C| / sqrt(A^2 + B^2)
    return abs(A * pb[0] + B * pb[1] + C) / ((A**2 + B**2) ** 0.5)


def simplify_path(path: Path) -> Path:
    raw = path.points
    simplified = []
    for i in range(len(raw)):
        simplified.append(raw[i])

        if i >= 2:
            next = simplified[-1]
            center = simplified[-2]
            previous = simplified[-3]
            # Calculate the distance from the center point to the line defined by previous and next points
            dist = distance_to_line(previous, next, center)
            if dist < 1.5:
                # If the distance is less than 0.5, we can remove the center point
                simplified.pop(-2)
                #print(f"Removed point {center} due to distance {dist:.2f} < 0.5")

            
  #  simplified.append(raw[-1])

    print("simplified path length:", len(simplified))
    p = Path()
    p.points = simplified
    return p


def convert_path_from_dstring(path_def, quality=9) -> Path:
   # path = parse_path(path_def)
    res = Path()

    res = raw_svg_path(path_def)
    res = simplify_path(res)

    return res

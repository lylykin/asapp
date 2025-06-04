
import svg.path
from sys import exit
from svg.path import parse_path
import math
import fast_math
class Path: 
    points: list[tuple[float, float]]

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




def douglas_peucker(points, epsilon):
    dmax = 0
    index = 0

    end = len(points) - 1
    for i in range(1, end):
        d = distance_to_line(points[0], points[end], points[i])
        if d > dmax:
            index = i
            dmax = d
    
    if dmax >= epsilon:
        # Recursive call
        left = douglas_peucker(points[:index + 1], epsilon)
        right = douglas_peucker(points[index:], epsilon)

        return left[:-1] + right
    else:
        return [points[0], points[end]]
    
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

    simplified = douglas_peucker(raw,3)  # Simplify the path using the Douglas-Peucker algorithm with a threshold of 1.5
    
            #else: 
            #    theta_1 = fast_math.fast_atan2(previous[1] - center[1], previous[0] - center[0])
            #    theta_2 = fast_math.fast_atan2(next[1] - center[1], next[0] - center[0])
            #    # If the angle between the previous and next points is too small, we can remove the center point
            #    if abs(theta_1 - theta_2) < 0.1:
            #        simplified.pop(-2)
           

    # print svg format:
    
    #for i, point in enumerate(raw):
    #    x, y = point
    #    if i == 0:
    #        print(f"M {x} {y}", end=" ")
    #    else:
    #        print(f"L {x} {y}", end=" ")
    #print("Z")  # Close the path #        print(f"Removed point {center} due to angle {abs(theta_1 - theta_2):.2f} < 0.1")

            
  #  simplified.append(raw[-1])

    #print("simplified path length:", len(simplified))
    p = Path()
    p.points = simplified
    return p


def convert_path_from_dstring(path_def, quality=9) -> Path:
   # path = parse_path(path_def)
    res = Path()

    res = raw_svg_path(path_def)
    res = simplify_path(res)

    return res

def get_path_box(pathList: list[Path]) -> tuple[float, float, float, float]:
    """
    Get the bounding box of a list of paths.
    Returns (x_min, y_min, x_max, y_max)
    """
    x_min = 0
    y_min = 0
    x_max = 109
    y_max = 109
    for path in pathList:
        for point in path.points:
            x, y = point
            if x < x_min:
                x_min = x
            if y < y_min:
                y_min = y
            if x > x_max:
                x_max = x
            if y > y_max:
                y_max = y


    return (x_min, y_min, x_max, y_max)

def constrain(pathList: list[Path], target_x_max = 109, target_y_max = 109):
    
    """
    Resize the path to fit within the specified maximum dimensions.
    """
    current_box = get_path_box(pathList)
    x_min, y_min, x_max_current, y_max_current = current_box

    width = x_max_current - x_min 
    height = y_max_current - y_min 
    scaling = 0
    if target_x_max / width < target_y_max / height: 
        scaling = target_x_max / width 
    else: 
        scaling = target_y_max / height 
    
    for path in pathList:
        for i, point in enumerate(path.points):
            x, y = point
            x = (x - x_min) * scaling
            y = (y - y_min) * scaling
            path.points[i] = (x, y)
    

    

    
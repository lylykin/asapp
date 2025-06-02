import math
import fast_math
from svg_path import Path
class PointExtended: 
    x: float
    y: float 
    curvature: float 
    theta: float 

    def __init__(self, x: float, y: float, curvature: float = 0.0, theta: float = 0.0):
        self.x = x
        self.y = y
        self.curvature = curvature
        self.theta = theta
    
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y}, curvature={self.curvature}, theta={self.theta})"

class PathExtended: 
    points_ex: list[PointExtended]


# https://stackoverflow.com/questions/41144224/calculate-curvature-for-3-points-x-y
def curvature(a: tuple[float,float], b: tuple[float,float], c: tuple[float, float]): 
    l1 = ((a[0]-b[0])**2 + (a[1]-b[1])**2)
    l2 = ((b[0]-c[0])**2 + (b[1]-c[1])**2)
    l3 = ((a[0]-c[0])**2 + (a[1] - c[1])** 2)

    area = 0.5 * abs(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
    if area <= 0.001:
        return 0  # Points are collinear, curvature is undefined
    return 4 * area * fast_math.inv_sqrt(l1 * l2 * l3)
#    return 4 * (area)/(l1*l2*l3)

# ok soit: 
# A / (sqrt(L1²) * sqrt(L2²) * sqrt(L3²))
# A / (sqrt(L1² * L2² * L3²))
# A * inv_sqrt(L1² * L2² * L3²)

# inv_sqrt est plus rapide que sqrt, donc on va l'utiliser



def angle(a: tuple[float, float], b: tuple[float, float]) -> float:
    """
    Calculate the angle in radians between two points a and b.
    """

    
    dx = b[0] - a[0]
    dy = b[1] - a[1]

    if dx == 0 and dy == 0:
        return 0.0
    
    return math.atan2(dy, dx)


def generate_extended_path(path: Path):
    points = path.points
    ex_points = []
    for i in range(len(points)):
        theta = 0
        if i < len(points) - 1:
            theta = angle(points[i], points[i+1])
        else: 
            theta = angle(points[i], points[i-1])
        

        curvature_value = 0.0
        if len(points) >=3:
            if i < len(points) - 2:
                curvature_value = curvature(points[i], points[i+1], points[i+2])
            elif i == len(points) - 2:
                curvature_value = curvature(points[i], points[i+1], points[i-1])
            else:
                curvature_value = curvature(points[i], points[i-1], points[i-2])

        print(f"Point {i}: ({points[i][0]}, {points[i][1]}) - Curvature: {curvature_value:.4f}, Theta: {theta:.4f}")
        ex_points.append(PointExtended(points[i][0], points[i][1], curvature_value, theta))

    res = PathExtended()
    res.points_ex = ex_points 
    return res 

        
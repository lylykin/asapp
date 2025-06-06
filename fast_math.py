import numpy as np

import math
# calcul de la racine carrée inverse 
# https://ajcr.net/fast-inverse-square-root-python/ 
def inv_sqrt(number):
    threehalfs = 1.5
    x2 = number * 0.5
    y = np.float32(number)
    
    i = y.view(np.int32)
    i = np.int32(0x5f3759df) - np.int32(i >> 1)
    y = i.view(np.float32)
    
    y = y * (threehalfs - (x2 * y * y))
    return float(y)

def fast_atan2(y, x):
    """
    Fast approximation of atan2 using numpy.
    """
    return np.arctan2(y, x)

# https://stackoverflow.com/questions/1878907/how-can-i-find-the-smallest-difference-between-two-angles-around-a-point 
def smallest_delta_angle(x, y):
    a = (x - y) % (math.pi/2)
    b = (y - x) % (math.pi/2)
    return abs(-a if a < b else b)

import svg.path
from sys import exit
from svg.path import parse_path

def convert_path(path_def):
    res = parse_path(path_def)

    for segment in res:

        print(segment)

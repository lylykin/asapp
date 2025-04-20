import json 
from xml.dom import minidom

from svg_path import convert_path


file2kanji = {}

kanji_db = {}

class Kanji: 
    name: str
    stroke_count: int

    def __init__(self, name: str):
        self.name = name 





def parse_kanji(kanji_file: str):
    doc = minidom.parse(f'data/kanji/{kanji_file}')  # parseString also exists
    path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
    doc.unlink()
    
    for path in path_strings:
        #print(path)
        convert_path(path)
        # do something with the path string
        # e.g. save it to a file or process it further




with open("./data/kvg-index.json") as f:
    d = json.load(f)
    
    f.close() 


length = len(d.keys())

i = 0
for kanjis in d.keys():
    print(f"adding kanji: {kanjis} with file: {d[kanjis][-1]} ({i}/{length})")
    parse_kanji(d[kanjis][-1])
    i += 1
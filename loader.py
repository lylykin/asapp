import json 
from xml.dom import minidom

from svg_path import convert_path_from_dstring, Path


file2kanji = {}

kanji_db = {}

class Kanji: 
    name: str
    stroke_count: int
    stokes: list[Path]

    def __init__(self, name: str):
        self.name = name 
        self.strokes = []
    
    def add_stroke(self, stroke: Path):
        self.strokes.append(stroke)
        self.stroke_count = len(self.strokes)




def parse_kanji(chr: str, kanji_file: str) -> Kanji:
    
    kanji = Kanji(chr)
    
    doc = minidom.parse(f'data/kanji/{kanji_file}') 
    path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
    doc.unlink()
    
    for path in path_strings:
        kanji.add_stroke(convert_path_from_dstring(path))


    return kanji



with open("./data/kvg-index.json") as f:
    d = json.load(f)
    
    f.close() 


length = len(d.keys())




i = 0
for kanjis in d.keys():
    print(f"adding kanji: {kanjis} with file: {d[kanjis][-1]} ({i}/{length})")
    kanji_db[kanjis] = parse_kanji(kanjis, d[kanjis][-1])

    i += 1
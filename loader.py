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

    def point_count(self):
        count = 0
        for stroke in self.strokes:
            count += len(stroke.points)
        return count


def parse_kanji(chr: str, kanji_file: str) -> Kanji:
    
    kanji = Kanji(chr)
    
    doc = minidom.parse(f'data/kanji/{kanji_file}') 
    path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
    doc.unlink()
    
    for path in path_strings:
        kanji.add_stroke(convert_path_from_dstring(path))


    return kanji



# compute from svg list to precomputed_json 
def compute_data():

    with open("./data/kvg-index.json") as f:
        d = json.load(f)
    
        f.close() 
    
    i = 0

    length = len(d.keys())
    for kanjis in d.keys():
        print(f"adding kanji: {kanjis} with file: {d[kanjis][-1]} ({i}/{length})")
    
        kanji_db[kanjis] = parse_kanji(kanjis, d[kanjis][-1])
        i += 1


    with open("./data/kanji_db.json", "w") as f:
        json.dump(kanji_db, f, default=lambda o: o.__dict__, indent=0, ensure_ascii=False)
        f.close()
    print("done")


# load points data from precomputed_json
def load_data():
    kanji_db = {}
    with open("./data/kanji_db.json", "r") as f:
        kanji_db = json.load(f)
        f.close()
    
    print("done")

    return kanji_db
kanji_db = load_data()
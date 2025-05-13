import json 
from xml.dom import minidom

from svg_path import convert_path_from_dstring, Path

from kanji import Kanji, KanjiDB

def parse_kanji(chr: str, kanji_file: str) -> Kanji:
    kanji = Kanji(chr, 0, [])
    
    # parse the dstring path
    doc = minidom.parse(f'data/kanji/{kanji_file}') 
    path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
    doc.unlink()

    # convert the dstring path to a list of strokes
    for path in path_strings:
        kanji.add_stroke(convert_path_from_dstring(path))

    return kanji

# compute from svg list to precomputed_json 
def compute_kanji_cache():

    kanji_db = {}
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
    return kanji_db

# load points data from precomputed_json
def load_kanji_cache():
    print("loading cached kanji_db.json")

    kanji_db = {}
    with open("./data/kanji_db.json", "r", encoding="utf-8") as f:
        kanji_db = json.load(f)
        f.close()
    
        print("done")
    
    return kanji_db


KanjiDB.the().update_kanji_db(load_kanji_cache())

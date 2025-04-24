from svg_path import convert_path_from_dstring, Path

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


# Quelque bidouillages pour que la base de données de kanji soit un singleton
# Car en réalité on a toujours une unique base de données de kanji
# ça sert a rien d'en créer plusieurs dans le code. 
# Donc c'est plus cohérent que ce soit un singleton.
class KanjiDB(object):
    _instance = None
    _kanji_stroke_db = {}
    _kanji_db = {}

    def __init__(self):
        raise Exception("Cette classe est un singleton ! Veuillez utiliser la méthode 'KanjiDB.the()' pour obtenir une instance.")
                
    def _update_stroke_db(self):
        for v in self._kanji_db.values():
            l = self._kanji_stroke_db.get(v.stroke_count, [])
            l.append(v)

    def update_kanji_db(self, new_kanji_db):
        self._kanji_db = new_kanji_db
        self._update_stroke_db()

    def kanji_from_char(self, chr: str) -> Kanji:
        if chr in self._kanji_db:
            return self._kanji_db[chr]
        else:
            raise ValueError(f"Kanji {chr} not found in database")
    
    # méthode du singleton, the() prise shamelessly des codings styles de serenityOS 
    @classmethod
    def the(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        return cls._instance
    
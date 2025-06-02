from svg_path import convert_path_from_dstring, Path

class Kanji: 
    name: str
    stroke_count: int
    strokes: list[Path]

    def __init__(self, name: str, strokes: list[Path], stroke_count: int = 0):
        self.name = name 
        self.strokes = strokes
        self.stroke_count = stroke_count
    
    def add_stroke(self, stroke: Path):
        '''
        Ajout d'un objet trait à l'objet kanji, adaptant le nombre de traits stockés
        '''
        self.strokes.append(stroke)
        self.stroke_count = len(self.strokes)

    def point_count(self):
        '''
        Calcul de la quantité de points total du kanji
        '''
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
            print(v)
            l = self._kanji_stroke_db.get(v.stroke_count, [])
            l.append(v)

    def update_kanji_db(self, new_kanji_db):
        for k, v in new_kanji_db.items():
            if k not in self._kanji_db:
                strokes = []
                
                for stroke in v["strokes"]:
                    strokes.append(Path())
                    for point in stroke["points"]:
                        strokes[-1].append(point)
                
                self._kanji_db[k] = Kanji(v["name"], strokes, v["stroke_count"])
            else:
                raise ValueError(f"Kanji {k} already exists in database")

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
    
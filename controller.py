from kanji import Kanji, KanjiDB
from dtw import Dtw
from dictionary import Dictionnary
from appWindow import App
from svg_path import Path
from identifier import *

class Controller :
    app : App
    db : KanjiDB

    def __init__(self, app : App, db : KanjiDB = KanjiDB.the()):
        self.app = app
        self.db = db

        self.app.compare_button.bind("<Button-1>", self.identify)

    def identify(self,event):
        client_strokes = self.app.strokes
        #print(client_strokes)
        kanji_2_id = Kanji("Unid")
        for s in client_strokes.values():
            p_stroke = Path()
            p_stroke.points = s
            kanji_2_id.add_stroke(p_stroke)
        kanji_matches = kanjiIdenfier(kanji_2_id,self.db)
        
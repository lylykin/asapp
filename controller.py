from kanji import Kanji, KanjiDB
from dictionary import Dictionary
from appWindow import App
from svg_path import Path
from identifier import *
from math import floor

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
        
        #ici, on doit changer pour n'avoir que 5 points
        for s in client_strokes.values():
            p_stroke = Path()
            p_stroke.points = [s[pt] for pt in range(0, len(s), floor(len(s)/5))] 
            kanji_2_id.add_stroke(p_stroke)
        return kanjiIdentifier(kanji_2_id,self.db)


    
        
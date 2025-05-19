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
        self.reduction_value = 10 # Distance euclidienne en dessous de laquelle les points tracés sont ignorés

        self.app.compare_button.bind("<Button-1>", self.identify)

    def identify(self,event):
        client_strokes = self.reduce_dotlist_size(self.app.strokes, self.reduction_value)
        #print(client_strokes)
        kanji_2_id = Kanji("Unid")
        
        #ici, on doit changer pour n'avoir que 5 points
        for s in client_strokes.values():
            p_stroke = Path()
            p_stroke.points = [s[pt] for pt in range(0, len(s), floor(len(s)/5))] 
            kanji_2_id.add_stroke(p_stroke)
        return kanjiIdentifier(kanji_2_id,self.db)
    
    def reduce_dotlist_size(self, dotlist, d_min = 10) :
        '''
        Réduit le nombre de points d'une liste de points en les séparant à la distance euclidienne de d_min pixels au minimum
        dotlist : list
        sous la forme [(x,y),(x,y),...]
        '''
        reduced_dotlist = dotlist.copy()
        if len(reduced_dotlist) > 1 : # La liste doit contenir au moins 2 points
            i = 1 # Parcours la liste en prenant le point à la position i et celui à i-1
            while i < len(reduced_dotlist) :
                x1, y1 = reduced_dotlist[i-1]
                x2, y2 = reduced_dotlist[i]
                dist = self.euclidian_distance(x1, y1, x2, y2)
                if dist < d_min :
                    reduced_dotlist.pop(i)
                else :
                    i += 1
        return reduced_dotlist
            
    
    def euclidian_distance(self, x1, y1, x2, y2):
        '''
        Etablit la distance euclidienne entre deux points sous la forme (x, y) selon leurs coordonnées
        '''
        vecteur = [x2-x1, y2-y1]
        return (vecteur[0]**2 + vecteur[1]**2)**0.5
from kanji import Kanji, KanjiDB
from dictionary import Dictionary
from svg_path import Path
from identifier import *
from math import floor



class Controller :
    db : KanjiDB
    dico : Dictionary

    def __init__(self, db : KanjiDB = KanjiDB.the(), dico : Dictionary = Dictionary.the()):
        self.db = db
        self.reduction_value = 10 # Distance euclidienne en dessous de laquelle les points tracés sont ignorés
        self.dico = dico



    def identify(self,strokes):
        kanji_2_id = Kanji("Unid",strokes= [])
        print(strokes)
        #ici, on doit changer pour n'avoir que 5 points
        for s in strokes.values():
            p_stroke = Path()
            p_stroke.points = [s[pt] for pt in range(0, len(s), floor(len(s)/5))] 
            kanji_2_id.add_stroke(p_stroke)
        return kanjiIdentifier(kanji_2_id,self.db)
    
    def kanji_tr_tabswitch(self, event, kanji : Kanji):
        pass


    def reduce_dotlist_size(self, dotlist) :
        '''
        Réduit le nombre de points d'une liste de points en les séparant à la distance euclidienne de d_min pixels au minimum
        dotlist : list
        sous la forme [(x,y),(x,y),...]
        '''
        d_min = self.reduction_value
        reduced_dotlist = dotlist.copy()
        for stroke in reduced_dotlist.keys():
            if len(reduced_dotlist[stroke]) > 1 : # La liste doit contenir au moins 2 points
                i = 1 # Parcours la liste en prenant le point à la position i et celui à i-1
                while i < len(reduced_dotlist[stroke]) :
                    x1, y1 = reduced_dotlist[stroke][i-1]
                    x2, y2 = reduced_dotlist[stroke][i]
                    dist = self.euclidian_distance(x1, y1, x2, y2)
                    if dist < d_min :
                        reduced_dotlist[stroke].pop(i)
                    else :
                        i += 1
        return reduced_dotlist
            
    
    def euclidian_distance(self, x1, y1, x2, y2):
        '''
        Etablit la distance euclidienne entre deux points sous la forme (x, y) selon leurs coordonnées
        '''
        vecteur = [x2-x1, y2-y1]
        return (vecteur[0]**2 + vecteur[1]**2)**0.5
    
'''
class TransTopLevel(ctk.CTkToplevel):
    kanji_name : str
    translation : str

    def __init__(self, kanji : Kanji, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kanji_name = kanji.name
        self.translation = self.dico.get_fr_translation(self.kanji_name)
        text = f"{self.kanji_name} :\n{self.translation}"
        self.label = ctk.CTkLevel(self, text=text)
        self.label.pack(padx=5, pady=5)
'''


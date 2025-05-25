from kanji import Kanji, KanjiDB
from dictionary import Dictionary
from svg_path import Path
import identifier
from math import floor



class Controller :

    def __init__(self, dico : Dictionary = Dictionary()):
        self.reduction_value = 10 # Distance euclidienne en dessous de laquelle les points tracés sont ignorés
        self.dico = dico

    def identify(self,strokes):
        '''
        Recieves a set of strokes and outputs the closest matching kanji in the database based on a DTW algorithm
        '''
        n_points = 6
        kanji_2_id = Kanji("Unid",strokes= [])
        print(strokes)
        #ici, on doit changer pour n'avoir que 5 points
        for s in strokes.values():
            p_stroke = Path()
            if len(s)>n_points:
                p_stroke.points = [s[pt] for pt in range(0, len(s), floor(len(s)/n_points))] 
            else :
                # Failsafe si la courbe avait moins de 5 points
                p_stroke.points = s
            kanji_2_id.add_stroke(p_stroke)
        return identifier.kanjiIdentifier(kanji_2_id)   

    def kanji_tr_tabswitch(self, tab, tab_name_list, kanji : str):
        '''
        Used when clicking on a proposed kanji frame to switch tab and show its translation
        '''
        tab.set(tab_name_list[1])
        # tab.entry  Missing editable entry for user to input text
        tab.display_kanji_dictionary(kanji)

    def drawing_offset(self, dotlist : dict):
        '''
        Finds the upper-left corner limit coordinates of user drawing and offsets all points to 'move' the drawing to the upper-left corner of canvas
        '''
        x_points = []
        y_points = []
        offset_dotlist = {}
        for stroke_points in dotlist.values():
            for point in stroke_points:
                x_points.append(point[0])
                y_points.append(point[1])
        x_min, y_min = min(x_points), min(y_points)
        
        for stroke,points in dotlist.items():
            offset_points = [(p[0]-x_min,p[1]-y_min) for p in points]
            offset_dotlist[stroke] = offset_points
    
        return offset_dotlist
        
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



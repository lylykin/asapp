from kanji import Kanji, KanjiDB
from dictionary import Dictionary
from svg_path import Path, simplify_path, constrain
import opti_identifier as identifier
from math import floor




class Controller :

    def __init__(self, dico : Dictionary = Dictionary()):
        self.reduction_value = 10 # Distance euclidienne en dessous de laquelle les points tracés sont ignorés
        self.dico = dico
        self.translator = Dictionary()

    def identify(self,strokes):
        '''
        Recieves a set of strokes and outputs the closest matching kanji in the database based on a DTW algorithm
        '''
        n_points = 9
        kanji_2_id = Kanji("Unid",strokes= [])
        print(strokes)
        #ici, on doit changer pour n'avoir que n_points points

        paths = []
        for s in strokes.values():
            p_stroke = Path()
            p_stroke.points = s
            if s != []: #failsafe et opti si liste de points vide, ajoute que les listes de points non vides
                p_stroke = simplify_path(p_stroke)
                paths.append(p_stroke)
                

        constrain(paths)


        for p_stroke in paths:
            
            p_stroke = simplify_path(p_stroke)

            s = p_stroke.points
            if len(s)>n_points:
                p_stroke.points = [s[pt] for pt in range(0, len(s), floor(len(s)/n_points))] 
            
            
            kanji_2_id.add_stroke(p_stroke) # Ajoute le trait à l'objet kanji à identifier
            # final len: 
            print(f"Stroke {len(kanji_2_id.strokes)} : {len(p_stroke.points)} points")

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
        if x_points != [] : # Failsafe si aucun points tracés
            for stroke_points in dotlist.values():
                for point in stroke_points:
                    x_points.append(point[0])
                    y_points.append(point[1])
            x_min, y_min = min(x_points), min(y_points)
        
            for stroke,points in dotlist.items():
                offset_points = [(p[0]-x_min,p[1]-y_min) for p in points]
                offset_dotlist[stroke] = offset_points
        else : 
            offset_dotlist = dotlist
    
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

    def translate_describe(self, word):
        '''
        Renvoie la traduction du mot dans l'autre langue ainsi que la description du mot sous la forme (trad, desc)
        '''
        trad = self.translator.get_fr_translation(word) # Récupère la traduction fr du mot jap et sa desc
        desc = self.translator.get_meaning("fr", word)
        if trad == None: # Si aucune traduction trouvée, cherche la traduction jap du mot fr et sa desc
            trad = self.translator.get_jp_translation(word)
            desc = self.translator.get_meaning("ja", word)
            if trad == None: # Si aucune traduction trouvée, le mot est considéré inexistant, renvoie une erreur
                trad = "Erreur : aucune correspondance trouvée"
                desc = ""
        return trad, desc


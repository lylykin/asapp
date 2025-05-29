from dtw import Dtw
from kanji import Kanji, KanjiDB
from svg_path import Path
import operator



def kanjiIdentifier(kanji_2_id : Kanji, kanji_file =KanjiDB.the()):
    """
    returns the closest kanjis according to dtw, compares kanji_2_id and the kanjis in the file
    Parameters : kanji_2_id (kanji) and kanji_file (json file) treated like an singleton (containing all the possible kanjis to compare)
    """
    
    kandict = {}
    stroke_count = kanji_2_id.stroke_count
    
    for kan in kanji_file._kanji_db.values() : # For each kanjis objects of the file   
        # first checking the number of strokes to avoid useless calculus. 
        # Adds the characters which have the same amount of strokes as kanji_2_id
        if stroke_count == kan.stroke_count:
            kandict[kan] = 0
            
    # n-ième trait à comparer avec le dtw
    n = 0 
    kandict = dtwKanji(kanji_2_id, kandict) # Comparer le trait n du kanji_2_id au trait n de tous les kanji de kandict (même nombre de trait)
        
    if len(kandict.keys()) == 0 : 
        return "Error : no matches found"
    else :
        for a, b in kandict.items() :
            print(f"key : {a.name}, score : {b}\n")
        sorted_kanjis = dict(sorted(kandict.items(), key=operator.itemgetter(1)))
        return [k.name for k in sorted_kanjis.keys()] # Renvoie la liste des caractères sélectionnés, triés par score DTW croissant
        


def lerp(va, vb, factor):
    """
    Lerp function from vA when factor is 0 and vB when factor is 1 
    it smoothly blend between the two value. 
    """
    return (1-factor) * va + factor * vb
    
def dtwStroke(stroke : Path,comp_stroke : Path):
    """
    returns the dtw score between 2 strokes
    """        
    return Dtw(stroke.points, comp_stroke.points).dtw()

def dtwKanji(kanji_2_id : Kanji, kandict : dict) : 
    """
    urmom
    """
    
    keys = kandict.keys()
    stroke_number = kanji_2_id.stroke_count
    
    #dtw d'un kanji : on fait le dtw stroke par stroke, puis on met que son score dtw est la moyenne des scores stroke par stroke
    for kan in keys:
        somme = 0
        print(kan.name)
        
        for i in range (stroke_number) : 
            somme += dtwStroke(kanji_2_id.strokes[i], kan.strokes[i])
            #si le score dépasse déjà la valeur min, ne sert à rien de la calculer, le score sera trop grand
     

        kandict[kan] = somme
                          
    return kandict
    
    
    
    

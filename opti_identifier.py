from dtw import Dtw
from kanji import Kanji, KanjiDB
from svg_path import Path
import operator
from path_extended import generate_extended_path, PathExtended

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


        # sort in a list by the value and return a list of key sorted

        for k,v in (kandict.items()):
            print(f"kanji {k.name} : {v}")
        sorted_kandict = sorted(kandict.copy().items(), key=operator.itemgetter(1))
 
        sorted_kandict = [k[0].name for k in sorted_kandict]
       # dump 
       # for i in range(len(sorted_kandict)):
        #     print(f"{i+1} : {sorted_kandict[i]}  ({kandict[sorted_kandict[i]]})")
        print("Sorted kandict :")
        for i, k in enumerate(sorted_kandict):
            print(f"{i+1} : {k}")
        
        sorted_kandict = sorted_kandict[:20]  # Keep only the 10 closest kanjis
        return sorted_kandict


def lerp(va, vb, factor):
    """
    Lerp function from vA when factor is 0 and vB when factor is 1 
    it smoothly blend between the two value. 
    """
    return (1-factor) * va + factor * vb
    
def dtwStroke(stroke : PathExtended,comp_stroke : PathExtended, ceiling: float) -> float:
    """
    returns the dtw score between 2 strokes
    """        
    return Dtw(stroke.points_ex, comp_stroke.points_ex).dtw(ceiling)

def dtwKanji(kanji_2_id : Kanji, kandict : dict) : 
    """
    urmom
    """
    
    res = {}
    keys = kandict.keys()
    stroke_number = kanji_2_id.stroke_count
    
    opti_stroke = []
    for i in range(stroke_number):
        opti_stroke.append(generate_extended_path(kanji_2_id.strokes[i]))
    #dtw d'un kanji : on fait le dtw stroke par stroke, puis on met que son score dtw est la moyenne des scores stroke par stroke

    last_max_v = float("inf")
    
    for kan in keys:
        somme = 0
        print(kan.name)
        
        for i in range (stroke_number) : 
            somme += dtwStroke(opti_stroke[i], generate_extended_path(kan.strokes[i]), last_max_v)
            #si le score dépasse déjà la valeur min, ne sert à rien de la calculer, le score sera trop grand
     
        if len(res.keys()) < 20:
            res[kan] = somme
        else: 

            max_v  = float("-inf")
            max_id = 0
            for k in res.keys():
                # select the max one, swap if needed 
                if res[k] > max_v:
                    max_v = res[k]
                    max_id = k
            if somme < max_v:
                last_max_v = max_v
                res.pop(max_id)
                res[kan] = somme
        
                          
    return res
    
    
    
    

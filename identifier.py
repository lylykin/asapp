from dtw import Dtw
from kanji import Kanji, KanjiDB
import math
from svg_path import Path

#note : this way of implementing could allow us to update the app to show all of the closest kanjis.
#note : attention : this file isnt debbuged!!!!!!
#note : A#6

def kanjiIdentifier(kanji_2_id : Kanji, kanji_file =KanjiDB.the()):
    """
    returns which Kanji it is
    Parameters : kanji_2_id (kanji) and kanji_file (json file)
    """
    
    kandict = {}
    n = 0
    stroke_count = kanji_2_id.stroke_count
    
    for kan in kanji_file._kanji_db.values() :        
        #first checking the number of strokes to avoid useless calculus.
        if stroke_count == kan.stroke_count:
            kandict[kan] = math.inf

    #shortening the number of kanjis until we looked for all the strokes or ended on 1 kanji. check how the stokes attributes is made, im not sure it works that way
    while len(kandict.keys())> 1 or n<stroke_count : 
        print(n)
        kandict = dtwStroke(kanji_2_id.strokes[n],n, kandict)
        n+=1
        
    if len(kandict.keys()) == 0 : 
        return "Error : no matches found"
    elif len(kandict) == 1 : 
        return kandict.keys[0].name
    else : 
        return "Error, there is more than 1 candidante and i don't know how to treat this situation yet"
        

def dtwStroke(stroke : Path, stroke_number : int, kandict : dict):
    """
    update the dico of the candidates kanji 
    """
    
    #strokes dtw calcul
    for kan in kandict.keys(): 
        print(kan.name) 
        kandict[kan] = Dtw(stroke.points, kan.strokes[stroke_number].points).dtw()
      
    dtw_min = min(kandict.values())
    
    for k,val in kandict.items() : 
        if val > dtw_min : 
            kandict.pop(k)
    
    return kandict
    
    

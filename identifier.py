from dtw import Dtw
from kanji import Kanji
import math

#note : this way of implementing could allow us to update the app to show all of the closest kanjis.
#note : attention : this file isnt debbuged!!!!!!
#note : A#6

def kanjiIdentifier(kanji_2_id : Kanji, kanji_file = Kanji.KanjiDB.the()):
    """
    returns which Kanji it is
    Parameters : kanji_2_id (kanji) and kanji_file (json file)
    """
    
    kandict = {}
    n = 0
    
    for kan in kanji_file : 
        #we have to convert it into a kanji object. to fill depending on how the json file is made.
        kan = Kanji()
        stroke_count = kanji_2_id.stroke_count
        
        #first checking the number of strokes to avoid useless calculus.
        if stroke_count == kan.stroke_count:
            kandict[kan] = math.inf

    #shortening the number of kanjis until we looked for all the strokes or ended on 1 kanji. check how the stokes attributes is made, im not sure it works that way
    while len(kandict).keys()> 1 or n<stroke_count : 
        kandict = dtwStroke(kanji_2_id.strokes[n],n, kandict)
        
    if len(kandict.keys()) == 0 : 
        return "Error : no matches found"
    elif len(kandict) == 1 : 
        return kandict.keys[0].name
    else : 
        return "Error, there is more than 1 candidante and i don't know how to treat this situation yet"
        

def dtwStroke(stroke : list, stroke_number : int, kandict : dict):
    """
    update the dico of the candidates kanji 
    """
    
    #strokes dtw calcul
    for kan in kandict.keys():  
        kandict[kan] = Dtw.dtw(stroke, kan.strokes[stroke_number])
      
    dtw_min = min(kandict.values())
    
    for k,val in kandict.items() : 
        if val > dtw_min : 
            kandict.pop(k)
    
    return kandict
    
    

from dtw import Dtw
from kanji import Kanji, KanjiDB
import math
from svg_path import Path

#note : this way of implementing could allow us to update the app to show all of the closest kanjis.
#note : attention : this file isnt debbuged!!!!!!
#note : A#6

def kanjiIdentifier(kanji_2_id : Kanji, kanji_file =KanjiDB.the()):
    """
    returns which Kanji it is according to dtw, compares kanji_2_id and the kanjis in the file
    Parameters : kanji_2_id (kanji) and kanji_file (json file) treated like an singleton (containing all the possible kanjis to compare)
    """
    
    kandict = {}
    stroke_count = kanji_2_id.stroke_count
    
    for kan in kanji_file._kanji_db.values() : # For each kanjis objects of the file   
        # first checking the number of strokes to avoid useless calculus. 
        # Adds the characters which have the same amount of strokes as kanji_2_id
        if stroke_count == kan.stroke_count:
            kandict[kan] = math.inf

    #shortening the number of kanjis until we looked for all the strokes or ended on 1 kanji. check how the stokes attributes is made, im not sure it works that way
    n = 0 # n-ième trait à comparer avec le dtw
    while len(kandict.keys()) > 1 or n < stroke_count : 
        print(n)
        kandict = dtwStroke(kanji_2_id.strokes[n],n, kandict) # Comparer le trait n du kanji_2_id au trait n de tous les kanji de kandict (même nombre de trait)
        n+=1 # Conservant les meilleurs candidats pour le trait n uniquement, va comparer le trait n+1 (s'il existe)
        
    if len(kandict.keys()) == 0 : 
        return "Error : no matches found"
    elif len(kandict) == 1 : 
        return [ x for x in kandict.keys()][0].name # /!\ EXPLIQUEZ name
    else : 
        return "Error, there is more than 1 candidante and i don't know how to treat this situation yet"
        

def dtwStroke(stroke : Path, stroke_number : int, kandict : dict):
    """
    update the dico of the candidates kanji according to the dtw algorithm, keeping the best candidates for a given stroke
    """
    keys = kandict.keys() # Tous les kanjis à traiter par dtw du nombre de trait stroke_number
    
    # Donne le score dtw de corrélation entre le trait à comparer et chaque traits de référence n°stroke_number
    for kan in keys: 
        print(kan.name) 
        kandict[kan] = Dtw(stroke.points, kan.strokes[stroke_number].points).dtw()
    
      
    dtw_min = min(kandict.values()) # Relève le score le plus bas (meilleure corrélation)
    
 
    items = kandict.copy().items() # Paires (kanji object, dtw score)

    # Réduit le dico des kanjis de même nombre de traits à tous ceux de score dtw minimal
    for k,val in items : 
        if val > dtw_min : 
            kandict.pop(k)
    
    return kandict
    
    

from dtw import Dtw
from kanji import Kanji, KanjiDB
from svg_path import Path



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

    # shortening the number of kanjis until we looked for all the strokes or ended on 1 kanji.
    n = 0 # n-ième trait à comparer avec le dtw
    while len(kandict.keys()) > 1 and n < stroke_count : 
        print(f"stroke {n}") # DEBUG
        print([k.name for k in kandict.keys()]) # DEBUG
        kandict = dtwStroke(kanji_2_id.strokes[n],n, kandict) # Comparer le trait n du kanji_2_id au trait n de tous les kanji de kandict (même nombre de trait)
        n += 1 # Conservant les meilleurs candidats pour le trait n uniquement, va comparer le trait n+1 (s'il existe)
        
    if len(kandict.keys()) == 0 : 
        return "Error : no matches found"
    else :
        sorted_kanjis = sorted(kandict, key=kandict.get)
        return [k.name for k in sorted_kanjis] # Renvoie la liste des caractères sélectionnés, triés par score DTW croissant
        


def lerp(va, vb, factor):
    """
    Lerp function from vA when factor is 0 and vB when factor is 1 
    it smoothly blend between the two value. 
    """
    return (1-factor) * va + factor * vb
    

def dtwStroke(stroke : Path, stroke_number : int, kandict : dict):
    """
    update the dico of the candidates kanji according to the dtw algorithm, keeping the best candidates for a given stroke
    """
    keys = kandict.keys() # Tous les kanjis à traiter par dtw du nombre de trait stroke_number
    

    tolerance = 0.7 # Valeur délimitant la limite haute pour le choix des kanji à garder selon leur score DTW

    # Donne le score dtw de corrélation entre le trait à comparer et chaque traits de référence n°stroke_number
    
    summed = 0
    for kan in keys:
        kandict[kan] += Dtw(stroke.points, kan.strokes[stroke_number].points).dtw()
        summed += kandict[kan]
      
    dtw_min = min(kandict.values()) # Relève le score le plus bas (meilleure corrélation)
    #dtw_max = (kandict.values())
    avg = summed / len(kandict.values())

    items = kandict.copy().items() # Paires (kanji object, dtw score)

    # Réduit le dico des kanjis de même nombre de traits à tous ceux de score dtw acceptable
    for k,val in items : 
        if val > lerp(dtw_min, avg, tolerance): # Elimine les kanji de score supérieur à une valeur entre le min et la moyenne
            kandict.pop(k)
    

    
    return kandict
    
    

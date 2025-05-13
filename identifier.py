import dtw
from kanji import Kanji
import json


#brainstorm de ce que j'ai besoin de faire : d'abord nombre de traits, puis stroke par stroke. 
#On compare par rapport à la database kanji_db, donc besion d'un loader
#pour comparer un stroke, DTW.

with open('.\data\kanji_db.json') as f : 
    #bon apparamment loader le fait, mais on verra avec cyp
    kanji_file = json.__loader__(f)
    
    

def kanjiIdenfier(kanji_2_id : Kanji, kanji_file):
    #ta mère est tellement fat qu'il faut opti le dtw. Sinon voir si l'id_kanji est un kanji ou si j'en fais un Kanji pour faciliter
    for kan in kanji_file : 
        if isStrokeNumberSame(kanji_2_id, kan) :
            #le continue eest provisoire c'est juste pour moi ne vous en occupez pas
            continue
                #try exept ou if else, à voir
        print("Learn to write, your Kanji doesnt match anything")
    
    
    pass

def isStrokeNumberSame(id_kanji : Kanji, test_kanji : Kanji) : 
    return test_kanji.stroke_count == id_kanji.stroke_count

def isSameStroke(id_kanji, test_kanji) : 
        
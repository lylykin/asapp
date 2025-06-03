#le but de ce fichier est de permettre à l'user d'apprendre à écrire un kanji voulu.
from kanji import Kanji
from dtw import Dtw
import time

#bon, en vrai plutot à mettre dans la partie appwindow directement, n'a pas de sens comme ca

class writeTeacher() : 
    kanji : Kanji
    
    def __init__(self, kanji : Kanji):
        """
        kanji est le kanji cliqué/ entré par l'user
        """
        pass
        #self.ref_strokes = kanji.strokes
    
    def write_teacher(self, stroke_list : list) : 
        """
        """
        #pour l'instant est aléatoire, à voir les ordres de grandeur des traits, mais en gros si est vraiment pas correct,
        #c'est que c'est pas le bon trait ou pas dans le bon sens
        correct_score = 100
        incorrect_index =''
        
        for n in range(self.kanji.stroke_count) : 
            score = Dtw().dtw(self.kanji.strokes[n], stroke_list[n])
            
            if score > correct_score : 
                incorrect_index+= str(n)+' ,'

        if incorrect_index == '' : 
            return ("Bien joué, vous avez correctement écrit le kanji!")
        else : 
            return("Erreur : les traits " + incorrect_index + "sont mal tracés. Vous pouvez réessayer")
            
        
            
    

            
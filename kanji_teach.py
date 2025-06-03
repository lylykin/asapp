#le but de ce fichier est de permettre à l'user d'apprendre à écrire un kanji voulu.
from kanji import Kanji
from dtw import Dtw

#bon, en vrai plutot à mettre dans la partie appwindow directement, n'a pas de sens comme ca

class writeTeacher() : 
    kanji : Kanji
    
    def __init__(self, kanji : Kanji):
        """
        kanji est le kanji cliqué/ entré par l'user
        """
        self.kanji = kanji
        #self.ref_strokes = kanji.strokes
    
    def stroke_teacher(self, stroke, number : int) : 
        """
        """
        if number >= self.kanji.stroke_number : 
            raise ValueError(f"le numéro du trait est incorrect : le kanji ne contient que {self.kanji.stroke_number} traits")
        else :
            #pour l'instant est aléatoire, à voir les ordres de grandeur des traits, mais en gros si est vraiment pas correct,
            #c'est que c'est pas le bon trait ou pas dans le bon sens
            correct_score = 100
            ref_stroke = self.kanji.strokes[number] 
            score = Dtw(ref_stroke, stroke).dtw()
            
            while score > correct_score : 
                return ("ce n'est pas le bon trait, réésayez")

            
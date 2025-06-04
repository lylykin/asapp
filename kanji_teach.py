#le but de ce fichier est de permettre à l'user d'apprendre à écrire un kanji voulu.
from kanji import Kanji
from dtw import Dtw


#bon, en vrai plutot à mettre dans la partie appwindow directement, n'a pas de sens comme ca

class writeTeacher() : 
    kanji : Kanji
    speed : float
    
    def __init__(self, kanji : Kanji, speed = 0.5):
        """
        kanji est le kanji cliqué/ entré par l'user
        """
        self.speed = speed
        self.kanji = kanji
    
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
        
    def teacher_time(self, time) : 
        """retourne la partie du kanji qui doit être écrite en fonction du temps écoulé"""

        
        write_stroke = [[] for _ in range (self.kanji.stroke_count)]
        step_time,s,p = 0,0,0
        
        while step_time != time  :
            
            if p >= len(self.kanji.strokes[s]) :
                s +=1
                p = 0
                write_stroke[s].append (self.kanji.strokes[s][p])    
                step_time += self.speed
                
            else : 
                write_stroke[s].append (self.kanji.strokes[s][p])    
                step_time += self.speed    
                p+=1
                
        return write_stroke
    
    def total_write_time(self):
        """
        le temps total pour l'écire est vitesse*nb points
        """
        count = 0
        for s in self.kanji.strokes : 
            for p in self.kanji.strokes[s] :
                count +=1
        
        return count*self.speed
    
    def stroke_write_time(self, n : int) -> float:
        """
        Retourne le temps qu'il faut pour écrire le n -ième stroke
        """
        
        if n >= len(self.kanji.stroke_count) : 
            raise IndexError(f"Erreur, le numéro du trait est trop grand : {n} (max : {len(self.kanji.stroke_count-1)})")
        
        else : 
            stroke = self.kanji.strokes[n]
            return len(stroke)*self.speed
        
        
        
            
    

            
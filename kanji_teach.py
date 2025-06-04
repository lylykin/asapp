#le but de ce fichier est de permettre à l'user d'apprendre à écrire un kanji voulu.
from kanji import Kanji
from dtw import Dtw


#bon, en vrai plutot à mettre dans la partie appwindow directement, n'a pas de sens comme ca

class writeTeacher() : 
    kanji : Kanji
    speed : float
    
    def __init__(self, kanji : Kanji, speed = 1.0):
        """
        kanji est le kanji cliqué/ entré par l'user
        """
        self.speed = speed
        self.kanji = kanji
    
    def lerp(self, point_a : tuple[float, float], point_b : tuple[float, float], factor):
        """
        Lerp function from vA when factor is 0 and vB when factor is 1 
        it smoothly blend between the two value. 
        """
        return ((1-factor) * point_a[0] + factor * point_b[0],(1-factor) * point_a[1] + factor * point_b[1])
    
    def write_teacher(self, stroke_list : list) : 
        """
        """
        #pour l'instant est aléatoire, à voir les ordres de grandeur des traits, mais en gros si est vraiment pas correct,
        #c'est que c'est pas le bon trait ou pas dans le bon sens
        correct_score = 100
        incorrect_index =''
        
        for n in range(self.kanji.stroke_count) : 
            score = Dtw().dtw(self.kanji.strokes.points[n], stroke_list[n])
            
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
        
        while step_time <= time  :
            
            if p >= len(self.kanji.strokes[s].points) :
                s +=1
                
                if s>= self.kanji.stroke_count: 
                    return None
                
                p = 0
                write_stroke[s].append (self.kanji.strokes[s].points[p]) 
                #print(f'write_stroke : {write_stroke}')   
                step_time += self.speed
                
            else : 
                write_stroke[s].append (self.kanji.strokes[s].points[p])  
              #  print(f'write_stroke : {write_stroke}')                   
                step_time += self.speed    
                p+=1
            
        
        return [elt for elt in write_stroke if elt != []]
    
    def total_write_time(self):
        """
        le temps total pour l'écire est vitesse*nb points
        """
        time = 0
        for i in range(len(self.kanji.strokes)) : 
            time += self.stroke_write_time(i)
        return time
    
    def stroke_write_time(self, n : int) -> float:
        """
        Retourne le temps qu'il faut pour écrire le n -ième stroke
        """
        
        if n >= self.kanji.stroke_count : 
            raise IndexError(f"Erreur, le numéro du trait est trop grand : {n} (max : {len(self.kanji.stroke_count-1)})")
        
        else : 
            stroke = self.kanji.strokes[n]
            return len(stroke.points)*self.speed
        
        
        
            
    

            
from kanji import Kanji
from dtw import Dtw


class writeTeacher() : 
    kanji : Kanji
    speed : float
    
    def __init__(self, kanji : Kanji, speed = 1.0):
        """
        kanji est le kanji cliqué/ entré par l'user
        speed : vitesse d'écriture
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
        Attention, méthode non implémentée.
        Vérifie que les traits donnés en entrée on été correctement écrits
        """
        
        # Valeur palier. Si le score est au-dessus, cela veut dire que le trait est mal écrit/ que ce n'eeest pas le bon trait
        #la valeur du palier est arbitraire car la fonction n'est pas utilisée. 
        correct_score = 100
        incorrect_index =''
        
        #calcul du score DTW pour chaque trait
        for n in range(self.kanji.stroke_count) : 
            score = Dtw().dtw(self.kanji.strokes.points[n], stroke_list[n])
            
            #ajout dans la liste des traits incorrectement écrits
            if score > correct_score : 
                incorrect_index+= str(n)+' ,'

        if incorrect_index == '' : 
            return ("Bien joué, vous avez correctement écrit le kanji!")
        else : 
            return("Erreur : les traits " + incorrect_index + "sont mal tracés. Vous pouvez réessayer")
        
    def teacher_time(self, time) : 
        """retourne la partie du kanji qui doit être écrite en fonction du temps écoulé"""

        #initialisation
        write_stroke = [[] for _ in range (self.kanji.stroke_count)]
        step_time,s,p = 0,0,0
        
        while step_time <= time  :
            
            #cas où on arrive à la fin d'un trait et doit papsser au suivant
            if p >= len(self.kanji.strokes[s].points) :
                s +=1
                
                if s>= self.kanji.stroke_count: 
                    return None
                
                p = 0
                write_stroke[s].append (self.kanji.strokes[s].points[p]) 
                step_time += self.speed
                
            else : 
                write_stroke[s].append (self.kanji.strokes[s].points[p])                    
                step_time += self.speed    
                p+=1
            
        #suppression des éléments vides non utilisés, créés lors de l'initialisation
        return [elt for elt in write_stroke if elt != []]
    
    def total_write_time(self):
        """
        retourne le temps nécessaire pour écrire 1 caractère entier
        """
        time = 0
        for i in range(len(self.kanji.strokes)) : 
            time += self.stroke_write_time(i)
        return time
    
    def stroke_write_time(self, n : int) -> float:
        """
        Retourne le temps qu'il faut pour écrire le n -ième stroke
        """
        #erreur-proofing
        if n >= self.kanji.stroke_count : 
            raise IndexError(f"Erreur, le numéro du trait est trop grand : {n} (max : {len(self.kanji.stroke_count-1)})")
        
        else : 
            stroke = self.kanji.strokes[n]
            return len(stroke.points)*self.speed
        
        
        
            
    

            
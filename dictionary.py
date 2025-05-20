#might be useful later?
"""
import json

with open('\data\kvg-index.json') as f : 
    dict_index = json.load(f)
"""

class Dictionary(object) : 
    _instance = None

#je considère que le dictionnaire fait francais/ japonais
    
    def __init__(self):
        self.j2f_dict = {}
        self.f2j_dict = {}

    def add_dict(self, j_word : str, fr_word : str) : 
        """
        Pour ajouter un mot dans le dictionnaire
        """
        self.f2j_dict[fr_word] = j_word
        self.j2f_dict[j_word] = fr_word
        
    def get_fr_translation(self, j_word) : 
        """returns the french translation in the dico"""
        if j_word in self.j2f_dict.keys() : 
            return self.j2f_dict[j_word] 
        
        else : 
            return "erreur : ce mot n'est pas dans le dictionnaire"
        
    def get_jp_translation(self, fr_word) : 
        """returns the japanese translation in the dico"""
        if fr_word in self.j2f_dict.keys() : 
            return self.j2f_dict[fr_word] 
        
        else : 
            return "erreur : ce mot n'est pas dans le dictionnaire"       
                
    @classmethod
    def the(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        return cls._instance
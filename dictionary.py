from PyMultiDictionary import MultiDictionary

#bon en fait la librairie fait tout, pas besoin de ca rip mon code 
class Dictionary() : 
    multi_dico : MultiDictionary

#je considère que le dictionnaire fait francais/ japonais
    
    def __init__(self):
        self.multi_dico = MultiDictionary()
        
    def get_fr_translation(self, j_word : str) : 
        """returns the french translation in the dico"""
        #errors are supported by the lib
        return self.multi_dico.translate('jp', j_word, to='fr')
        
    def get_jp_translation(self, fr_word :str) : 
        """returns the japanese translation in the dico"""
        return self.multi_dico.translate("fr", fr_word, to="jp")
      
                
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
        return self.multi_dico.translate('ja', j_word, to='fr')
        
    def get_jp_translation(self, fr_word :str) : 
        """returns the japanese translation in the dico"""
        return self.multi_dico.translate("fr", fr_word, to="ja")
    
    def get_meaning(self, language:str, word:str):
        """
        returns the description of the current word
        meaning renvoie un tuple contenant
        - une liste de string (caracteristics_list) : ['verb','noun',]
        - un string avec 2 phrases séparées par un point, anglais puis la langue du mot
        - un string vide
        """
        caracteristics_list, eng_lang_desc, empty = self.multi_dico.meaning(language, word)
        desc_items = eng_lang_desc.split('.')
        possible_eng_descs = []
        for item in desc_items :
            if item.isascii():
                possible_eng_descs.append(item)
        return possible_eng_descs, eng_lang_desc

#debugdic = Dictionary()
#print(debugdic.get_jp_translation("C"))
#print(debugdic.get_fr_translation("車"))
#print(debugdic.get_meaning("ja","車"))
# C'est de la grosse merde ce dictionnaire, vraiment cette lib elle dégage               
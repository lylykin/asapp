import asyncio
from googletrans import Translator

class Dictionary() : 
    trans : Translator

    #je considère que le dictionnaire fait francais/ japonais
    
    def __init__(self):
        self.trans = Translator()
        
    #permet de tout avoir en sychrone en restant sur le même thread
    def async2sync(self,await_func) :
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(await_func)
    
    #requête de la traduction à l'API Google    
    async def _get_translation(self, word : str, src_lang : str, dest_lang : str) :  
        return await self.trans.translate(word, dest=dest_lang, src=src_lang)
        
    def get_jp_translation(self, fr_word :str) : 
        """returns the japanese translation in the dico"""
        translated = self.async2sync(self._get_translation(fr_word, 'fr', 'ja'))
        return translated.text, translated.pronunciation
        
    def get_fr_translation(self, jp_word : str) :
        """ retourne la traduction française d'un mot""" 
        translated = self.async2sync(self._get_translation(jp_word, 'ja', 'fr'))
        return translated.text, translated.pronunciation
    
    async def _get_language(self, word):
        return await self.trans.detect(word)
    
    def translate_language(self, word):
        """
        retourne la traduction en francais ou en japonais, en fonction de la langue détectée
        """
        jp_trans, jp_pronun = self.get_jp_translation(word)
        fr_trans, fr_pronun = self.get_fr_translation(word)
        if word == jp_trans:
            return fr_trans, fr_pronun
        else:
            return jp_trans, jp_pronun

#debugdic = Dictionary()
#print(debugdic.get_jp_translation("voiture"))
#print(debugdic.get_fr_translation("車"))
#print(debugdic.translate_language("comment"))
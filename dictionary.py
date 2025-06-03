import asyncio
from googletrans import Translator


class Dictionary() : 
    trans : Translator

#je considère que le dictionnaire fait francais/ japonais
    
    def __init__(self):
        self.trans = Translator()
        
    #permet de tout avoir en sychrone en restant sur le même thread pour facilter
    def async2sync(self,await_func) :
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(await_func)
    
        
    async def _get_translation(self, word : str, lang : str) :  
        return await self.trans.translate(word, dest=lang)
        
    def get_jp_translation(self, fr_word :str) : 
        """returns the japanese translation in the dico"""
        translated = self.async2sync(self._get_translation(fr_word, 'ja'))
        return translated.text
        
    
    def get_fr_translation(self, jp_word : str) : 
        translated = self.async2sync(self._get_translation(jp_word, 'fr'))
        return translated.text
    
    async def _get_language(self, word):
        return await self.trans.detect(word)
    
    def translate_language(self, word):
        lang = self.async2sync(self._get_language(word))
        lang = lang.lang
        if lang == "ja":
            return self.get_fr_translation(word), lang
        else:
            return self.get_jp_translation(word), "fr"
        #else :
        #    return "Aucun résultat", ""
   
#debugdic = Dictionary()
#print(debugdic.get_jp_translation("voiture"))
#print(debugdic.get_fr_translation("車"))
#print(debugdic.translate_language("comment"))
# C'est de la grosse merde ce dictionnaire, vraiment cette lib elle dégage               
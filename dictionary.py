import asyncio
from googletrans import Translator
from pylexique import Lexique383

#bon en fait la librairie fait tout, pas besoin de ca rip mon code 
class Dictionary() : 
    translator : Translator
    lexique : Lexique383

#je considère que le dictionnaire fait francais/ japonais
    
    def __init__(self):
        self.translator = Translator(service_urls=['translate.google.com'])
        self.lexique = Lexique383()

    async def get_translation(self, word :str):
        translation = None
        detection = await self.translator.detect(word)
        print(detection)
        lang = detection.lang
        conf = detection.confidence
        if conf < 0.3 : # Confiance insuffisante pour la langue
            print("Erreur : Langue non identifiée")
        else :
            if lang == "fr" : 
                translation = await self.get_jp_translation(word)
            elif lang == "ja" :
                translation = await self.get_fr_translation(word)
        return translation
      
    async def get_fr_translation(self, word : str) : 
        """returns the french translation in the dico"""
        #errors are supported by the lib
        return await self.translator.translate(word, dest="fr", src="ja")
        
    async def get_jp_translation(self, word :str) : 
        """returns the japanese translation in the dico"""
        return await self.translator.translate(word, dest="ja", src="fr")
    
    def get_lexicon(self, fr_word:str):
        """
        returns the lexicon of the current french word
        """
        word_lexicon = self.lexique.get_lex(fr_word)
        return word_lexicon

async def main():
    debugdic = Dictionary()
    print(await debugdic.get_jp_translation("bonjour"))
    print(await debugdic.get_fr_translation("車"))
    print(await debugdic.get_translation("bonjour")) # Détecte l'anglais à chaque fois pour raison obscure et prend pour source l'anglais
    print(debugdic.get_lexicon("bonjour"))

if __name__ == "__main__":
    asyncio.run(main()) # Je suis terrifé par l'utilisation de fonctions asynchrones
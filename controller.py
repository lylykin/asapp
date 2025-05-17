from kanji import Kanji, KanjiDB
from dtw import Dtw
from dictionary import Dictionnary
from appWindow import App
from svg_path import Path
from identifier import *

class Controller :
    app : App
    db : KanjiDB

    def __init__(self, app : App, db : KanjiDB = KanjiDB.the()):
        self.app = app
        self.db = db
        
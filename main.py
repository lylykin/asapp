from loader import compute_kanji_cache
from matplotlib import pyplot as plt
import sys
from controller import Controller
from appWindow import App

asapp = App()
control = Controller(asapp)
asapp.mainloop()


if len(sys.argv) < 2:
    print("Usage: python main.py <command>")
    print("Commands:")
    print("  compute: Compute cache data from kanji files (may take a while), already computed")
    sys.exit(0)    

if sys.argv[1] == "compute":

    compute_kanji_cache(   )
elif sys.argv[1] == "display":
    # Display the kanji data
    from kanji import KanjiDB
    from svg_path import convert_path_from_dstring, Path

    kanji_db = KanjiDB.the()._kanji_db
    kanji = kanji_db["日"]
    print(kanji.name)
    print(kanji.stroke_count)
    print(kanji.point_count())
    
    for stroke in kanji.strokes:
        plt.plot(*zip(*stroke.points))
    
    plt.show()
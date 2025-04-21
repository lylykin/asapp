from loader import compute_data
import sys



if len(sys.argv) < 2:
    print("Usage: python main.py <command>")
    print("Commands:")
    print("  compute: Compute data from kanji files")
    sys.exit(1)    

if sys.argv[1] == "compute":

    compute_data(   )
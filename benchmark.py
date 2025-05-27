from kanji import KanjiDB
from svg_path import convert_path_from_dstring, Path
import time 
import controller
import random
import loader




def benchmark(n, seed): 
    # generate random stroke from seed:
    strokes = {}
    ctrl = controller.Controller()
    random.seed(42 + seed)  # For reproducibility
    for i in range(n):
        strokes[i] = []
        px= 0
        py = 0
        for _ in range(0,50): 
            strokes[i].append((px,py))
            px += random.randint(-5,5)
            py += random.randint(-5,5)
    start_time = time.time()
    
    ctrl.identify(strokes)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to identify {n} strokes: {elapsed_time:.4f} seconds")
    return elapsed_time
if __name__ == "__main__":

    results = []
    deltas = []
    for n in range(1, 9):
        print(f"Benchmarking with {n} strokes:")
      
        run_results = []  
        for count in range(4):
            print(f"Run {count+1} for {n} strokes")
            # Run the benchmark
            run_results.append(benchmark(n, count))
            print("-" * 40)
        
        avg = sum(run_results) / len(run_results)
        avg_delta = 0
        for t in run_results:
            avg_delta += abs(t - avg)
        avg_delta /= len(run_results)

        print(f"Average time for {n} strokes over 10 runs: {avg:.4f} plus/minus {avg_delta:.4f} seconds")

           
        print("-" * 40)
        results.append((avg, avg_delta))
    print("Benchmark results:")
    n = 1
    for avg, avg_delta in results:
        print(f"Average({n:2}): {avg:.4f}, Delta: {avg_delta:.4f} seconds")
        n += 1
        
    

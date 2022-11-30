from random import shuffle
from algo import Algorithm
from func import solvable, output_puzzle
from config import starting_values, TIME
import threading
import time


def main():
    new = starting_values.copy()
    shuffle(new)
    while not solvable(new):
        shuffle(new)
    choice = int(input("1 for BFS, 2 for A*: "))
    starting_time = time.time()
    if choice == 1:
        thread = threading.Thread(target=lambda: output_puzzle(Algorithm(new).solve_bfs()))
    else:
        thread = threading.Thread(target=lambda: output_puzzle(Algorithm(new).solve_a()))
    thread.daemon = True
    thread.start()
    thread.join(TIME)
    if time.time() - starting_time > TIME:
        print(f"Time is up({TIME} sec).")


if __name__ == '__main__':
    main()

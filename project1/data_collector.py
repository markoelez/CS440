#!/usr/bin/env python3

import time
from repeated_astar import RepeatedAStar, AStarVariants, TieBreakVariants
from adaptive_astar import AdaptiveAStar
from world import World
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':

    NUM_GRID_WORLDS = 50
    GRID_WORLD_DIMENS = (101, 101)

    world = World(size=NUM_GRID_WORLDS, dimens=GRID_WORLD_DIMENS)
    world.load("data")

    d1 = []
    d2 = []

    d1_label = "Repeated Forwards"
    d2_label = "Adaptive"

    for i, grid in enumerate(world):
        print("\nITERATION: {}\n".format(i))
        print("=" * 50)
        start, goal = grid.get_start(), grid.get_goal()

        # Test 1
        a = time.time()
        astar = RepeatedAStar(None, grid, start, goal)
        astar.search(variant=AStarVariants.FORWARDS, tiebreak=TieBreakVariants.HI_G)
        b = time.time()
        d1.append([i, b - a])

        # Test 2
        a = time.time()
        astar = AdaptiveAStar(None, grid, start, goal)
        astar.search(variant=AStarVariants.FORWARDS, tiebreak=TieBreakVariants.HI_G)
        b = time.time()
        d2.append([i, b - a])
    
    print("=" * 50)
    print("\nDone, saving...\n")

    # save 
    np_d1 = np.asarray(d1)
    np_d2 = np.asarray(d2)
    
    d1_fn = d1_label.lower().replace(" ", "-") + ".csv"
    d2_fn = d2_label.lower().replace(" ", "-") + ".csv"

    np.savetxt(d1_fn, np_d1, delimiter=",")
    np.savetxt(d2_fn, np_d2, delimiter=",")
    
    x_d1 = [v[0] for v in d1]
    y_d1 = [v[1] for v in d1]

    x_d2= [v[0] for v in d2]
    y_d2 = [v[1] for v in d2]

    d1 = plt.scatter(x_d1, y_d1, color='k')
    d2 = plt.scatter(x_d2, y_d2, color='g')

    plt.xlabel('Grid Number', fontsize=18)
    plt.ylabel('Time Elapsed', fontsize=16)

    #plt.legend((d1, d2), ("Low G", "High G"))
    plt.legend((d1, d2), (d1_label, d2_label))
    plt.show()

    print("\n Save successful\n")

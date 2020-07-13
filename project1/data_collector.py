#!/usr/bin/env python3

import time
import sys
import pygame
from display import Display
from repeated_astar import RepeatedAStar, AStarVariants, TieBreakVariants
from adaptive_astar import AdaptiveAStar
from grid import Grid, load_grid
from cell import Cell, CellState
from world import World
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':

    NUM_GRID_WORLDS = 50
    GRID_WORLD_DIMENS = (101, 101)

    world = World(size=NUM_GRID_WORLDS, dimens=GRID_WORLD_DIMENS)
    world.load("data")

    lo = []
    hi = []
    
    for i, grid in enumerate(world):
        print("ITERATION: {}".format(i))
        start, goal = grid.get_start(), grid.get_goal()

        # Run low g and save times
        a = time.time()
        astar = RepeatedAStar(None, grid, start, goal)
        astar.search(variant=AStarVariants.FORWARDS, tiebreak=TieBreakVariants.LO_G)
        b = time.time()
        lo.append([i, b - a])

        # Run high g and save times
        a = time.time()
        astar = RepeatedAStar(None, grid, start, goal)
        astar.search(variant=AStarVariants.FORWARDS, tiebreak=TieBreakVariants.HI_G)
        b = time.time()
        hi.append([i, b - a])


    # Show graph
    lo = np.asarray(lo_g, dtype=np.float32)
    
    x_lo = [v[0] for v in lo]
    y_lo = [v[1] for v in lo]

    hi = np.asarray(hi_g, dtype=np.float32)

    x_hi = [v[0] for v in hi]
    y_hi = [v[1] for v in hi]

    plt.scatter(x_lo, y_lo, color='k')
    plt.scatter(x_hi, y_hi, color='g')
    plt.show()

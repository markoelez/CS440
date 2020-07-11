#!/usr/bin/env python3

import sys
from display import Display
from astar2 import AStar, AStarVariants
from grid import Grid, load_grid
from cell import Cell, CellState
from world import World
import pygame


NUM_GRID_WORLDS = 5#50

#GRID_WORLD_SIZE_W = 101
#GRID_WORLD_SIZE_H = 101
GRID_WORLD_SIZE_W = 90
GRID_WORLD_SIZE_H = 90 

GRID_WORLD_DIMENS = (GRID_WORLD_SIZE_W, GRID_WORLD_SIZE_H)


# Start by generating world with a set number of grids
world = World(size=NUM_GRID_WORLDS, dimens=GRID_WORLD_DIMENS)

# Save world in given directory
#world.save("data")
world.load("data")

# Ask user to choose a single grid from the generated world
grid_num = int(input("Choose a grid. Provide an integer index from 0 to {}:\n".format(NUM_GRID_WORLDS)))
# Validate input
if not isinstance(grid_num, int) or grid_num < 0 or grid_num >= NUM_GRID_WORLDS:
    raise ValueError("Provided index is out of range")

# Get grid
grid = world[grid_num]

# Get start and goal positions
start, goal = grid.get_start(), grid.get_goal()

# Initialize visual display
display = Display(grid)

# Start main loop
print("Instructions: \n")
print("Press 0 to reset the grid to its default state\n")
print("Press 1 to run repeated forward A* search from starting cell (green) to goal cell (red)\n")
print("Press 2 to run repeated backward A* search from goal cell (red) to start cell (green)\n")
print("Press q or esc tq or esc too quit the program\n")
print("Listening for input...")
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                print('Resetting grid...\n')
                display.reset_grid()
                pygame.display.flip()
            elif event.key == pygame.K_1:
                print('Running forwards A* Search\n')
                astar = AStar(display, start, goal)
                astar.search(variant=AStarVariants.FORWARDS)
                pygame.display.flip()
            elif event.key == pygame.K_2:
                print('Running backwards A* Search\n')
                astar = AStar(display, start, goal)
                astar.search(variant=AStarVariants.BACKWARDS)
                pygame.display.flip()
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                print('Quitting...\n')
                sys.exit(0)
    pygame.display.flip()


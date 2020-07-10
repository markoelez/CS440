#!/usr/bin/env python3

from display import Display
from astar import AStar
from grid import Grid, load_grid
from cell import Cell, CellState
from world import World
import pygame


NUM_GRID_WORLDS = 10#50

#GRID_WORLD_SIZE_W = 101
#GRID_WORLD_SIZE_H = 101
GRID_WORLD_SIZE_W = 90
GRID_WORLD_SIZE_H = 90 

GRID_WORLD_DIMENS = (GRID_WORLD_SIZE_W, GRID_WORLD_SIZE_H)


# Start by generating world with a set number of grids
world = World(size=NUM_GRID_WORLDS, dimens=GRID_WORLD_DIMENS)

# Save world in given directory
world.save("data")

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
print("Press 1 to run A* search from starting cell (green) to goal cell (red)...\n")
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                astar = AStar(display, start, goal)
                astar.do_forwards()
                pygame.display.flip()
                print('Running A* Search')

    pygame.display.flip()


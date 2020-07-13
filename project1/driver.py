#!/usr/bin/env python3

import time
import sys
from display import Display
from repeated_astar import RepeatedAStar, AStarVariants, TieBreakVariants
#from astar2 import RepeatedAStar, AStarVariants, TieBreakVariants
from grid import Grid, load_grid
from cell import Cell, CellState
from world import World
import pygame


NUM_GRID_WORLDS = 5#50
GRID_WORLD_SIZE_W = 101 
GRID_WORLD_SIZE_H = 101
"""
GRID_WORLD_SIZE_W = 5 
GRID_WORLD_SIZE_H = 5 
"""
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
"""
grid = Grid(5, 5)
for r in range(len(grid.maze)):
    for c in range(len(grid.maze[0])):
        tmp = grid.cell_at(r, c)
        tmp.set_state(CellState.FREE)
grid.maze[1][2].set_state(CellState.WALL)
grid.maze[2][2].set_state(CellState.WALL)
grid.maze[3][2].set_state(CellState.WALL)
grid.maze[2][3].set_state(CellState.WALL)
grid.maze[3][3].set_state(CellState.WALL)
grid.maze[4][3].set_state(CellState.WALL)

grid.maze[4][1].set_state(CellState.START)
grid.maze[4][4].set_state(CellState.END)

grid.start = grid.cell_at(4, 1)
grid.goal = grid.cell_at(4, 4)
"""
# Get start and goal positions
start, goal = grid.get_start(), grid.get_goal()

# Initialize visual display
display = Display(grid)

# Start main loop
print("="*60)
print("Instructions: \n")
print("Press 0 to reset the grid to its default state\n")
print("Press 1 to run repeated forward A* (tie-break high g) search from starting cell (green) to goal cell (red)\n")
print("Press 2 to run repeated forward A* (tie-break low g) search from starting cell (green) to goal cell (red)\n")
print("Press 3 to run repeated backward A* (tie-break high g) search from goal cell (red) to start cell (green)\n")
print("Press 4 to run repeated backward A* (tie-break low g) search from goal cell (red) to start cell (green)\n")
print("Press q or esc tq or esc too quit the program\n")
print("Listening for input...\n")
print("="*60)
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
                print('Running repeated forwards A* Search, tie-breaking on high g\n')
                astar = RepeatedAStar(display, start, goal)
                a = time.time()
                astar.search(variant=AStarVariants.FORWARDS, tiebreak=TieBreakVariants.HI_G)
                b = time.time()
                print("Finished running algorithm. Took {} seconds.\n".format(b - a))
                print("=" * 60)
                pygame.display.flip()
            elif event.key == pygame.K_2:
                print('Running repeated forwards A* Search, tie-breaking on low g\n')
                astar = RepeatedAStar(display, start, goal)
                a = time.time()
                astar.search(variant=AStarVariants.FORWARDS, tiebreak=TieBreakVariants.LO_G)
                b = time.time()
                print("Finished running algorithm. Took {} seconds.\n".format(b - a))
                print("=" * 60)
                pygame.display.flip()
            elif event.key == pygame.K_3:
                print('Running repeated backwards A* Search, tie-breaking on high g\n')
                astar = RepeatedAStar(display, start, goal)
                a = time.time()
                astar.search(variant=AStarVariants.BACKWARDS, tiebreak=TieBreakVariants.HI_G)
                b = time.time()
                print("Finished running algorithm. Took {} seconds.\n".format(b - a))
                print("=" * 60)
                pygame.display.flip()
            elif event.key == pygame.K_4:
                print('Running repeated backwards A* Search, tie-breaking on low g\n')
                astar = RepeatedAStar(display, start, goal)
                a = time.time()
                astar.search(variant=AStarVariants.BACKWARDS, tiebreak=TieBreakVariants.LO_G)
                b = time.time()
                print("Finished running algorithm. Took {} seconds.\n".format(b - a))
                print("=" * 60)
                pygame.display.flip()
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                print('Quitting...\n')
                sys.exit(0)
    pygame.display.flip()


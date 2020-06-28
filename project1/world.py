#!/usr/bin/env python3

from constants import GRID_WORLD_DIMENS, NUM_GRID_WORLDS
from grid import Grid

class World:

    def __init__(self, size=NUM_GRID_WORLDS, dimens=GRID_WORLD_DIMENS):
        self.w, self.h = dimens

        self.size = size

        self.grids = []

    def gen_grids(self):
        """
        Generate all maze-like grids in world.
        """
        for _ in range(self.size):
            self.grids.append(self.gen_grid())

    def gen_grid(self):
        """Generates a single grid."""
        return Grid(self.w, self.h)

    def print_all(self):
        """Print all grids in world."""
        for grid in self.grids:
            print(grid)
            print()
            print('=' * 70)
            print()


if __name__ == '__main__':

    #dimens = GRID_WORLD_DIMENS
    dimens = (30, 30)

    world = World(size=2, dimens=dimens)

    world.gen_grids()

    world.print_all()

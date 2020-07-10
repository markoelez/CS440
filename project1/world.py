#!/usr/bin/env python3

from constants import GRID_WORLD_DIMENS, NUM_GRID_WORLDS
from grid import Grid, load_grid

class World:

    def __init__(self, size=NUM_GRID_WORLDS, dimens=GRID_WORLD_DIMENS):
        self.w, self.h = dimens

        self.size = size

        self.grids = []

        self.gen_grids()

    def gen_grids(self):
        """Generate all maze-like grids in world."""
        
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

    def save(self, base_dir='data'):
        for i, grid in enumerate(self.grids):
            grid.serialize('{}/grid{}.pickle'.format(base_dir, i))

    def load(self, base_dir):
        for i in range(self.size):
            self.grids.append(load_grid('{}/grid{}.pickle'.format(base_dir, i)))

    def __getitem__(self, idx):
        return self.grids[idx]


if __name__ == '__main__':

    #dimens = GRID_WORLD_DIMENS
    dimens = (30, 30)

    world = World(size=2, dimens=dimens)

    world.save('data')

    test = World(size=2, dimens=dimens)

    test.load('data')

    test.print_all()

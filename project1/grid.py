#!/usr/bin/env python3

import random

class Grid:
    """Represents a maze of Cells."""
    def __init__(self, w, h):
        """Initialized with number of cells in each dimension"""
        self.w, self.h = w, h
        # internal grid representation
        self.maze = [[Cell(x, y) for y in range(self.h)] for x in range(self.w)]

    def get_cell(self, x, y):
        """Get Cell at position."""
        return self.maze[x][y]

    def __str__(self):
        """Simple representation for printing."""
        rows = ['-' * self.w * 2]
        for y in range(self.h):
            row = ['|']
            for x in range(self.w):
                if self.maze[x][y].walls['E']:
                    row.append(' |')
                else:
                    row.append('  ')
            rows.append(''.join(row))
            row = ['|']
            for x in range(self.w):
                if self.maze[x][y].walls['S']:
                    row.append('-+')
                else:
                    row.append(' +')
            rows.append(''.join(row))
        return '\n'.join(rows)

    def get_neighbors(self, cell):
        dirs = [('W', (-1, 0)),
                ('E', (1, 0)),
                ('S', (0, 1)),
                ('N', (0, -1))]

        neighbors = []
        for d, (dx, dy) in dirs:
            # Get new pos 
            x2, y2 = cell.x + dx, cell.y + dy
            # Check bounds
            if (0 <= x2 < self.w) and (0 <= y2 < self.h):
                n = self.get_cell(x2, y2)
                if n.walled_off():
                    neighbors.append((d, n))
        return neighbors

    def gen_maze(self):
        n = self.w * self.h
        stack = []
        curr = self.get_cell(0, 0)

        n_vis = 1

        while n_vis < n:
            neighbors = self.get_neighbors(curr)

            if not neighbors:
                curr = stack.pop()
                continue

            d, next_cell = random.choice(neighbors)
            curr.remove_wall(next_cell, d)
            stack.append(curr)
            curr = next_cell
            n_vis += 1


class Cell:
    """Represents a single cell in the grid."""

    # Walls separate cells from N-S and E-W
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        """Initialize Cell with given position and surrounded by walls."""
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def walled_off(self):
        """Check if walls in all directions"""
        return all(self.walls.values())

    def remove_wall(self, target, wall):
        # remove wall in origin
        self.walls[wall] = False
        # remove wall in target
        target.walls[self.wall_pairs[wall]] = False


if __name__ == '__main__':

    maze = Grid(10, 5)

    print(maze)

    print('=' * 20)
    maze.gen_maze()

    print('=' * 20)
    print(maze)

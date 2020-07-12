#!/usr/bin/env python3

import random
import pickle
from cell import Cell, CellState

class Grid:
    """Represents a maze of Cells."""
    def __init__(self, width, height):
        random.seed()
        """Initialized with number of cells in each dimension"""
        self.w, self.h = width, height
        # internal grid representation
        self.maze = [[Cell(x, y) for y in range(self.h)] for x in range(self.w)]
        # generate maze
        self.gen_maze()

    def get_rows(self):
        return self.w

    def get_cols(self):
        return self.h

    def get_dimens(self):
        return (self.get_rows(), self.get_cols())

    def get_cell(self, x, y):
        """Get Cell at position."""
        return self.maze[x][y]

    def __str__(self):
        """Simple representation for printing."""
        rows = []
        for y in range(self.h):
            row = []
            for x in range(self.w):
                row.append(str(self.cell_at(x, y)))
            rows.append(''.join(row))

        return '\n'.join(rows)

    def cell_at(self, x, y):
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            raise IndexError
        return self.maze[x][y]

    def get_neighbors(self, cell):
        """Returns list of neighbors for a given cell"""
        dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        res = []
        for (dx, dy) in dirs:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.w) and (0 <= y2 < self.h):
                n = self.cell_at(x2, y2)
                res.append(n)
        return res


    def get_valid_neighbors(self, cell, visited):
        """Returns list of unvisited neighbors for use in maze generation"""
        dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        res = []
        for (dx, dy) in dirs:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.w) and (0 <= y2 < self.h):
                if not visited[x2][y2]:
                    n = self.cell_at(x2, y2)
                    res.append(n)
        return res

    def gen_maze(self):
        visited = [[0 for y in range(self.h)] for x in range(self.w)]

        while not self.is_done(visited):
            # Choose random starting cell, mark as free space
            start = self.cell_at(random.randint(0, self.w - 1), random.randint(0, self.h - 1))
            start.set_state(CellState.FREE)

            self.dfs(start, visited)
        
        """
        # Choose random start and end
        start = self.cell_at(random.randint(1, self.w - 2), random.randint(1, self.h - 2))
        start.set_state(CellState.START)

        end = self.cell_at(random.randint(1, self.w - 2), random.randint(1, self.h - 2))

        # Ensure we never have the same start and end cells
        while start == end:
            end = self.cell_at(random.randint(1, self.w - 2), random.randint(1, self.h - 2))
        end.set_state(CellState.END)

        self.start = start
        self.goal = end 

        """
        self.start = self.cell_at(0, 0)
        self.goal = self.cell_at(self.get_rows() - 1, self.get_cols() - 1)

        self.start.set_state(CellState.START)
        self.goal.set_state(CellState.END)

    def is_done(self, visited):
        for row in visited:
            if 0 in row:
                return False
        return True

    def dfs(self, start, visited):
        stack = []
        stack.append(start)

        while stack:
            n = stack.pop()
            neighbors = self.get_valid_neighbors(n, visited)

            # Check for dead end
            if not neighbors:
                return

            neighbor = random.choice(neighbors)

            #if random.randint(0, 100) < 40:
            if random.random() < 40:
                # Mark as blocked
                neighbor.set_state(CellState.WALL)
            else:
                # Mark as unblocked and add to stack
                neighbor.set_state(CellState.FREE)
                stack.append(neighbor)

            visited[neighbor.x][neighbor.y] = 1

    def serialize(self, filename):
        with open(filename, 'wb') as output:
            pickle.dump(self, output)

    def get_start(self):
        return self.start

    def get_goal(self):
        return self.goal

def load_grid(filename):
    with open(filename, 'rb') as _input:
        return pickle.load(_input)


if __name__ == '__main__':

    maze = Grid(50, 30)

    #print(maze)

    #print('=' * 100)

    maze.serialize('test2.pickle')

    test = load_grid('test2.pickle')

    print(test)



#!/usr/bin/env python3

import pygame
from display import Display
from cell import Cell, CellState
from grid import Grid, load_grid
from heapq import *
from heap import MinHeap
from enum import Enum
from constants import BLACK, WHITE, GREEN, RED, YELLOW, BLUE, EXPLORE_COLOR


class AStarVariants(Enum):
    FORWARDS = 'forwards'
    BACKWARDS = 'backwards'


class AStar:

    def __init__(self, viewer, start, goal):

        self.viewer = viewer
        self.grid = viewer.get_grid() 
        self.grid_size = self.grid.get_rows()

        self.cols = self.grid.get_cols()
        self.rows = self.grid.get_rows()

        self.start = start
        self.og_start = start
        self.goal = goal 

        self.dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        self.open= MinHeap()
        self.closed = set()

        trace = {}

        self.gscore = {}
        self.fscore = {}
        self.hscore = {}

        self.tree = {}

        # Initialize search(s) = 0 
        self._search = {}
        for r in range(self.grid.get_rows()):
            for c in range(self.grid.get_cols()):
                self._search[self.grid.cell_at(r, c)] = 0
        self.counter = 0

    def heuristic(self, a, b):
        (x1, x2), (y1, y2) = a.get_pos(), b.get_pos()
        return abs(x1 - x2) + abs(y1 - y2)

    def h(self, start):
        """Utility for calculating h(s) from start to goal node"""
        return self.heuristic(start, self.goal)

    def search(self, variant=AStarVariants.FORWARDS):
        while self.start != self.goal:
            self.counter += 1
            self.gscore[self.start] = 0
            self._search[self.start] = self.counter
            self.gscore[self.goal] = float("inf")
            self._search[self.goal] = self.counter

            self.open.push((self.gscore[self.start] + self.h(self.start), self.start))

            self.compute_path()

            if not self.open:
                print("\nCan't find a path!\n")
                return  

            # Follow path until we reach goal or action cost increases
            curr = self.goal
            while curr != self.start:
                curr = self.tree[curr]
            
            # Set start to curr
            self.start = curr

        print("\nFound path\n")

    def compute_path(self):
        while self.open and self.gscore[self.goal] > min(self.gscore[self.start], self.h(self.start)):
            # Remove cell with smallest f-value
            s = self.open.pop()[1]
            print(s)
            self.viewer.draw_rect_at_pos(s.get_x(), s.get_y(), EXPLORE_COLOR)
            pygame.display.flip()
            # Expand cell
            self.closed.add(s)
            # Take all actions a in A(s)
            for (dx, dy) in self.dirs:
                (x, y) = (s.get_x() + dx, s.get_y() + dy)
                # check bounds
                if not (0 <= x < self.rows) or not (0 <= y < self.cols):
                    continue
                # Get succ(s, a)
                succ = self.grid.cell_at(x, y)
                # Check if wall
                if succ.is_state(CellState.WALL):
                    continue
                if self._search[succ] < self.counter:
                    self.gscore[succ] = float("inf")
                    self._search[succ] = self.counter
                if self.gscore[succ] > self.gscore[s] + 1:
                    self.gscore[succ] = self.gscore[s] + 1
                    # Trace
                    self.tree[succ] = s
                    #print("SUCC: {}, SELF.OPEN: {}\n".format(succ, self.open))
                    if succ in [x[1] for x in self.open]:
                        print("SUCC: ", succ)
                        idx = [x[1] for x in self.open].index(succ)
                        self.open.pop_at(idx)
                    
                    fsucc = self.gscore[succ] + self.h(succ)
                    self.open.push((fsucc, succ))


if __name__ == '__main__':

    grid = load_grid('{}/grid{}.pickle'.format("data", 0))

    viewer = Display(grid)

    start = grid.get_start()
    goal = grid.get_goal()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    print('Resetting grid...\n')
                    viewer.reset_grid()
                    pygame.display.flip()
                elif event.key == pygame.K_1:
                    print('Running forwards A* Search\n')
                    astar = AStar(viewer, start, goal)
                    astar.search(variant=AStarVariants.FORWARDS)
                    pygame.display.flip()
        pygame.display.flip()




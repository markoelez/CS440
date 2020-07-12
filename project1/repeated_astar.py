#!/usr/bin/env python3

import sys
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

class TieBreakVariants(Enum):
    LO_G = 'lowg'
    HI_G = 'hig'


class RepeatedAStar:

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

        self.no_color = set()
        self.no_color.add(self.start)
        self.no_color.add(self.goal)

        self.gscore = {}
        self.fscore = {}
        self.hscore = {}

        self.paths = []

        self.tree = {}

        self.explore_colors = [BLUE, EXPLORE_COLOR]

        # Initialize search(s) = 0 
        self._search = {}
        for r in range(self.grid.get_rows()):
            for c in range(self.grid.get_cols()):
                self._search[self.grid.cell_at(r, c)] = 0
        self.counter = 0

        # Initialize all action costs to 1
        self.action_costs = {}
        for r in range(self.grid.get_rows()):
            for c in range(self.grid.get_cols()):
                self.action_costs[self.grid.cell_at(r, c)] = 1

        self.tiebreak = TieBreakVariants.HI_G

    def heuristic(self, a, b):
        (x1, x2), (y1, y2) = a.get_pos(), b.get_pos()
        return abs(x1 - x2) + abs(y1 - y2)

    def h(self, start):
        """Utility for calculating h(s) from start to goal node"""
        return self.heuristic(start, self.goal)

    def backtrack(self, path):
        path = path[::-1]
        for n in path[:-1]:
            if n != self.start and n != self.goal:
                self.viewer.draw_rect_at_pos(n.get_x(), n.get_y(), YELLOW)
            pygame.display.flip()

    def search(self, variant=AStarVariants.FORWARDS, tiebreak=TieBreakVariants.HI_G):
        colors = (EXPLORE_COLOR, (153, 216, 208), (255, 202, 194))
        self.tiebreak = tiebreak
        if variant == AStarVariants.BACKWARDS:
            self.start, self.goal = self.goal, self.start
        path = []
        while self.start != self.goal:
            self.counter += 1

            self.gscore[self.start] = 0
            self.gscore[self.goal] = float("inf")

            self._search[self.start] = self.counter
            self._search[self.goal] = self.counter

            self.open = MinHeap()
            self.closed = set() 
            
            if self.tiebreak == TieBreakVariants.HI_G:
                self.open.push((self.gscore[self.start] + self.h(self.start), -self.gscore[self.start], self.start))
            else:
                self.open.push((self.gscore[self.start] + self.h(self.start), self.gscore[self.start], self.start))

            self.compute_path(colors[self.counter%3])

            if not self.open:
                print("\nCan't find a path!\n")
                return  
            
            # Follow path until we reach goal or action cost increases
            curr = self.goal
            path = []
            connect = [self.start]
            while curr and curr != self.start:
                path.append(curr)
                if curr in self.tree:
                    curr = self.tree[curr]

            # Follow path
            for curr in path[::-1]:
                if curr.blocked():
                    # Reached a wall, try again
                    print("Reached a wall")
                    self.viewer.draw_rect_at_pos(curr.get_x(), curr.get_y(), (246, 159, 124))
                    # Increase g score to infinity 
                    self.gscore[curr] = float("inf") 
                    # Update action cost
                    self.action_costs[curr] = float("inf")
                    break
                else:
                    # If unblocked, move start
                    connect.append(curr)
                    self.start = curr
                    self.no_color.add(curr)
            # Draw new starting cell in green
            self.viewer.draw_rect_at_pos(self.start.get_x(), self.start.get_y(), GREEN)
            # Connect start with end of this path
            self.backtrack(connect)
            self.no_color.add(self.start)

        #self.backtrack([i for sublist in self.paths for i in sublist])
        print("\nFound path\n")

    def compute_path(self, explore_color):
        print("Computing path...")

        while self.open.peek()[0] < self.gscore[self.goal]:
            # Remove cell with smallest f-value
            s = self.open.pop()[2]
            if s not in self.no_color and s != self.start and s != self.goal and not s.blocked():
                self.viewer.draw_rect_at_pos(s.get_x(), s.get_y(), explore_color)
                pygame.display.flip()
            # Check if cell already expanded
            if s in self.closed: continue
            # Expand cell
            self.closed.add(s)
            # Take all actions a in A(s)
            for (dx, dy) in self.dirs:
                (x, y) = (s.get_x() + dx, s.get_y() + dy)

                # check bounds
                if not (0 <= x < self.rows) or not (0 <= y < self.cols): continue

                # Get succ(s, a)
                succ = self.grid.cell_at(x, y)

                action_cost = self.action_costs[succ]

                if self._search[succ] < self.counter:
                    self.gscore[succ] = float("inf")
                    self._search[succ] = self.counter

                if self.gscore[succ] > self.gscore[s] + action_cost:
                    self.gscore[succ] = self.gscore[s] + action_cost
                    # Trace
                    self.tree[succ] = s
                    # Remove from open list 
                    if succ in [x[2] for x in self.open]:
                        idx = [x[2] for x in self.open].index(succ)
                        self.open.pop_at(idx)
                    
                    fsucc = self.gscore[succ] + self.h(succ)
                    if self.tiebreak == TieBreakVariants.HI_G:
                        self.open.push((fsucc, -self.gscore[succ], succ))
                    else:
                        self.open.push((fsucc, self.gscore[succ], succ))


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




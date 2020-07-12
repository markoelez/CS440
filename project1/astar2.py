#!/usr/bin/env python3

import time
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
        
        # S, E, N, W
        self.dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

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
        print(a, b, a.get_pos(), b.get_pos(), abs(x1 - x2) + abs(y1 - y2))

        return abs(x1 - x2) + abs(y1 - y2)

    def h(self, start):
        """Utility for calculating h(s) from start to goal node"""
        #return self.heuristic(start, self.goal)
        return abs(start.get_x() - self.goal.get_x()) + abs(start.get_y() - self.goal.get_y())

    def backtrack(self, path):
        path = path[::-1]
        for n in path[:-1]:
            if n != self.og_start and n != self.goal:
                self.viewer.draw_rect_at_pos(n.get_x(), n.get_y(), YELLOW)
            pygame.display.flip()
    
    def look_around(self, start):
        blocked = []
        for (dx, dy) in self.dirs:
            try:
                tmp = self.grid.cell_at(self.start.get_x() + dx, self.start.get_y() + dy)
                if tmp.blocked():
                    self.action_costs[tmp] = float("inf")
                    blocked.append(tmp)
            except: 
                continue
        return blocked

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

            self.open.push((self.gscore[self.start] + self.h(self.start), -self.gscore[self.start], self.start))

            # Look around
            blocked = self.look_around(self.start)

            self.compute_path(blocked, colors[0])

            if not self.open:
                print("\nCan't find a path!\n")
                return  
            
            # Follow path until we reach goal or action cost increases
            curr = self.goal
            path = []
            connect = [self.start]
            print(curr, path, connect)
            while curr and curr != self.og_start:
                path.append(curr)
                if curr in self.tree:
                    curr = self.tree[curr]

            print("here")

            # Follow path
            for curr in path[::-1]:
                if curr.blocked():
                    # Reached a wall, try again
                    print("Reached a wall")
                    #self.viewer.draw_rect_at_pos(curr.get_x(), curr.get_y(), (246, 159, 124))
                    # Increase g score to infinity 
                    self.gscore[curr] = float("inf") 
                    # Update action cost
                    #self.action_costs[curr] = float("inf")
                    break
                else:
                    # If unblocked, move start
                    connect.append(curr)
                    self.start = curr
                    self.no_color.add(curr)
            # Rebase knowledge of adjacent cells
            blocked = self.look_around(self.start)
            # Draw new starting cell in green
            #self.viewer.draw_rect_at_pos(self.start.get_x(), self.start.get_y(), GREEN)
            # Connect start with end of this path
            #self.backtrack(connect)
            self.no_color.add(self.start)

        self.backtrack(path)
        print("\nFound path\n")

    def compute_path(self, blocked, explore_color):
        print("Computing path...")

        while self.open:
            time.sleep(0)
            print("EXPANDING : {}".format(self.open.peek()[2]))

            print(self.open)
            print("=" * 50)
            current = self.open.pop()[2]
            
            if not current in self.closed:
                self.closed.add(current)

            if not current.blocked() and current != self.start and current != self.goal and current not in self.no_color:
                self.viewer.draw_rect_at_pos(current.get_x(), current.get_y(), explore_color)

            pygame.display.flip()

            if current == self.goal:
                return

            for (dx, dy) in self.dirs:
                try:
                    neighbor = self.grid.cell_at(current.get_x() + dx, current.get_y() + dy)
                except:
                    continue
                
                # If in observed adjacent blocked cells
                if neighbor in blocked:
                    continue
                
                # Get g(n) -- distance from start node to n
                g = self.gscore[current] + self.action_costs[current]

                # Check bounds
                if not (0 <= neighbor.get_x() < self.grid_size) or not (0 <= neighbor.get_y() < self.grid_size):
                    continue

                # Check if visited
                if neighbor in self.closed and g >= self.gscore.get(neighbor, 0):
                    continue
                
                if g < self.gscore.get(neighbor, 0) or neighbor not in [i[2] for i in self.open]:
                    self.tree[neighbor] = current

                    self.gscore[neighbor] = g 
                    self.fscore[neighbor] = g + self.h(neighbor)

                    self.open.push((self.fscore[neighbor], self.gscore[neighbor], neighbor))


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




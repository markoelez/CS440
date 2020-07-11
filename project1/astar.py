#!/usr/bin/env python3

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

        self.start = start 
        self.goal = goal 

        self.f = {}
        self.h = None
        self.g = set()

    def heuristic(self, a, b):
        (x1, x2), (y1, y2) = a.get_pos(), b.get_pos()
        return abs(x1 - x2) + abs(y1 - y2)

    def search(self, variant=AStarVariants.FORWARDS):
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        close_set = set()
        open_set = MinHeap()
        trace = {}

        if variant == AStarVariants.BACKWARDS:
            self.start, self.goal = self.goal, self.start

        gscore = {self.start: 0}
        fscore = {self.start: self.heuristic(self.start, self.goal)}

        # Sort PQ based on f(x) value
        open_set.push((fscore[self.start], self.start))

        while open_set:
            # Pop cell of queue
            current = open_set.pop()[1]
            
            # If we have reached the goal, backtrack and show path
            if current == self.goal:
                # Draw start and goal back in
                self.viewer.draw_rect_at_pos(self.goal.get_x(), self.goal.get_y(), RED)
                self.viewer.draw_rect_at_pos(self.start.get_x(), self.start.get_y(), GREEN)

                path = []
                # Trace backwards
                while current in trace:
                    if current != self.start and current != self.goal:
                        self.viewer.draw_rect_at_pos(current.get_x(), current.get_y(), YELLOW)

                    self.viewer.update() path.append(current)

                    current = trace[current]

                return path 
            
            close_set.add(current)

            for (dx, dy) in dirs:
                # Get neighbor cell: exception raised if out of bounds
                try:
                    neighbor = self.grid.cell_at(current.get_x() + dx, current.get_y() + dy)
                except:
                    continue
                
                # Get g(n) -- distance from start node to n
                g = gscore[current] + self.heuristic(current, neighbor)

                # Get h(n) -- cost from n to goal
                self.h = self.heuristic(current, self.goal)

                # Check bounds
                if not (0 <= neighbor.get_x() < self.grid_size) or not (0 <= neighbor.get_y() < self.grid_size):
                    continue

                # Check if cell is blocked off 
                if self.grid.cell_at(neighbor.get_x(), neighbor.get_y()).is_state(CellState.WALL):
                    continue

                # Check if visited
                if neighbor in close_set and g >= gscore.get(neighbor, 0):
                    continue
                
                if g < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in open_set]:
                    # Update trace
                    trace[neighbor] = current

                    # Update g value
                    #self.g.add(g)

                    gscore[neighbor] = g 
                    fscore[neighbor] = g + self.heuristic(neighbor, self.goal)

                    self.viewer.draw_rect_at_pos(neighbor.get_x(), neighbor.get_y(), EXPLORE_COLOR)

                    self.viewer.update()
                    open_set.push((fscore[neighbor], neighbor))

        print('--- path not found ---')
        return False

if __name__ == '__main__':

    grid = load_grid('{}/grid{}.pickle'.format("data", 0))

    viewer = Display(grid)

    start_state = grid.get_start()
    goal_state = grid.get_goal()

    astar = AStar(viewer, start_state, goal_state)

    done = False
    while not done:
        done = astar.do_forwards()

        viewer.update()


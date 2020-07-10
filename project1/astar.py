#!/usr/bin/env python3

from display import Display
from cell import Cell, CellState
from grid import Grid, load_grid
from heapq import *

from constants import BLACK, WHITE, GREEN, RED, YELLOW, BLUE, EXPLORE_COLOR


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

    def do_forwards(self):
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        close_set = set()

        trace = {}

        gscore = {self.start: 0}

        fscore = {self.start: self.heuristic(self.start, self.goal)}

        open_set = []

        heappush(open_set, (fscore[self.start], self.start))

        while open_set:
            # Pop cell of queue
            current = heappop(open_set)[1]
            
            # If we have reached the goal, backtrack and show path
            if current == self.goal:
                path = []
                # Trace backwards
                while current in trace:
                    self.viewer.draw_rect_at_pos(current.get_x(), current.get_y(), YELLOW)

                    self.viewer.update()
                    path.append(current)

                    current = trace[current]
                return path 
            
            close_set.add(current)

            for (dx, dy) in neighbors:
                # Get neighbor cell
                try:
                    neighbor = self.grid.cell_at(current.get_x() + dx, current.get_y() + dy)
                except:
                    continue
            
                tentative_g_score = gscore[current] + self.heuristic(current, neighbor)

                # Get heuristic
                self.h = self.heuristic(current, self.goal)

                # Check bounds
                if not (0 <= neighbor.get_x() < self.grid_size) or not (0 <= neighbor.get_y() < self.grid_size):
                    print('out of bounds', self.grid_size, neighbor.get_x(), neighbor.get_y())
                    continue

                # Check if cell is blocked off 
                if self.grid.cell_at(neighbor.get_x(), neighbor.get_y()).is_state(CellState.WALL):
                    continue

                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in open_set]:

                    self.g.add(tentative_g_score)

                    trace[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + self.heuristic(neighbor, self.goal)

                    self.viewer.draw_rect_at_pos(neighbor.get_x(), neighbor.get_y(), EXPLORE_COLOR)

                    self.viewer.update()
                    heappush(open_set, (fscore[neighbor], neighbor))

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


#!/usr/bin/env python3

import pygame
from pygame.locals import DOUBLEBUF
from cell import Cell, CellState
from grid import Grid, load_grid
from constants import BLACK, WHITE, GREEN, RED, YELLOW, BLUE, EXPLORE_COLOR


#WIDTH = 40 
#HEIGHT = 40 
WIDTH = 20
HEIGHT = 20 

F = 22 

# Gap between cells in grid
GAP = 1


class Display:

    def __init__(self, grid):
        """Create a visual display from a given Grid object"""
        self.rows, self.cols = grid.get_rows(), grid.get_cols() 

        self.W, self.H = (self.rows * F) + 1, (self.rows * F) + 1
        
        self._grid = grid

        pygame.init()
        self.screen = pygame.display.set_mode((self.W, self.H), DOUBLEBUF)
        self.surface = pygame.Surface(self.screen.get_size())
        pygame.display.set_caption("Grid Display")

        self.draw_grid()

    def update(self):
        for _ in pygame.event.get():
            pass

        pygame.display.flip()

    def draw_rect_at_pos(self, r, c, color):
        """Draw a rect of given color at (row, col)"""
        x1 = ((GAP + WIDTH) * c + GAP)
        y1 = ((GAP + HEIGHT) * r + GAP)
        pygame.draw.rect(self.screen, color, (x1, y1, WIDTH, HEIGHT))

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                color = WHITE
                if self._grid.cell_at(row, col).is_state(CellState.WALL):
                    color = BLACK 
                elif self._grid.cell_at(row, col).is_state(CellState.END):
                    color = RED 
                elif self._grid.cell_at(row, col).is_state(CellState.START):
                    color = GREEN 

                self.draw_rect_at_pos(row, col, color)

        pygame.display.flip()

    def reset_grid(self):
        self.draw_grid()

    def get_grid(self):
        return self._grid

    def get_screen(self):
        return self.screen

    def get_rows(self):
        return self.rows


if __name__ == '__main__':

    grid = load_grid('{}/grid{}.pickle'.format("data", 0))

    viewer = Display(grid)

    while 1:
        viewer.update()


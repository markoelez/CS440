#!/usr/bin/env python3

import pygame
from pygame.locals import DOUBLEBUF
from cell import Cell, CellState
from grid import Grid, load_grid


WIDTH = 10
HEIGHT = 10

# Gap between cells in grid
GAP = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (135,206,235)

class Display:

    def __init__(self, grid):
        """Create a visual display from a given Grid object"""
        self.rows, self.cols = grid.get_rows(), grid.get_cols() 

        self.W, self.H = (self.rows * 11) + 1, (self.rows * 11) + 1
        
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

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                color = WHITE
                if self._grid.cell_at(row, col).is_state(CellState.WALL):
                    color = BLUE 
                elif self._grid.cell_at(row, col).is_state(CellState.END):
                    color = GREEN 
                elif self._grid.cell_at(row, col).is_state(CellState.START):
                    color = RED 

                pygame.draw.rect(self.screen, color,[(GAP+ WIDTH) * col + GAP, (GAP+ HEIGHT) * row + GAP, WIDTH, HEIGHT])

        pygame.display.flip()


if __name__ == '__main__':

    grid = load_grid('{}/grid{}.pickle'.format("data", 0))

    viewer = Display(grid)

    while 1:
        viewer.update()


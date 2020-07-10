#!/usr/bin/env python3

from enum import Enum


class CellState(Enum):
    FREE = '_'
    WALL = '*'

    START = 'S'
    END = 'G'

    UNSET = ' '

class Cell:
    """Represents a single cell in the grid."""

    def __init__(self, x, y, state=CellState.UNSET):
        """Initialize Cell with given position and state."""
        self.x, self.y = x, y
        # Initialize as unset 
        self.state = state

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_pos(self):
        return (self.x, self.y)
    
    def set_state(self, new_state):
        self.state = new_state

    def __str__(self):
        return "({}, {}) -- {}".format(self.x, self.y, self.state.value)
    
    def __hash__(self):
        return hash(str(self.x) + str(self.y) + str(self.x - self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def is_state(self, other_state):
        return self.state == other_state

    def __lt__(self, other):
        return self.get_x() < other.get_x()

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
    
    def set_state(self, new_state):
        self.state = new_state

    def __str__(self):
        return str(self.state.value)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

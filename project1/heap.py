import collections


class MinHeap:
    """Defines a binary heap"""

    def __init__(self):
        self.elements = collections.deque()
    
    def is_empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()

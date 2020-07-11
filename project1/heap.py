import heapq 


class MinHeap:
    """Defines a binary heap"""

    def __init__(self):
        self.array = []

    def is_empty(self):
        return len(self.array) == 0
    
    def push(self, x):
        """Push element onto queue"""
        heapq.heappush(self.array, x)
    
    def pop(self):
        """Pop smallest element off queue"""
        return heapq.heappop(self.array)

    def pop_at(self, i):
        self.array.pop(i)
        heapq.heapify(self.array)

    def remove(self, x):
        print('REMOVING: ', x, type(x))
        self.array.remove(x)

    def __getitem__(self, idx):
        return self.array[idx]

    def __str__(self):
        return ", ".join(map(str, self.array))

    def __len__(self):
        return len(self.array)



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

    def peek(self):
        if self.array:
            return self.array[0]

    def pop_at(self, i):
        self.array.pop(i)
        heapq.heapify(self.array)

    def remove(self, x):
        self.array.remove(x)

    def __getitem__(self, idx):
        return self.array[idx]

    def __str__(self):
        return "\nHEAP --------------------- START: \n" + "\n ".join(map(str, map(lambda x: "Cell: {}, F: {}, G: {}.".format(x[2], x[0], x[1]), self.array))) + "\nHEAP --------------------- END\n"

    def __len__(self):
        return len(self.array)



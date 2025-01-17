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
        heapq.heapify(self.array)

    def __getitem__(self, idx):
        return self.array[idx]

    def __str__(self):
        heapq.heapify(self.array)
        return "\nHEAP --------------------- START: \n" + "\n ".join(map(str, map(lambda x: "Cell: {}, F: {}, G: {}, H: {}.".format(x[2], x[0], x[1], x[0] - x[1]), self.array))) + "\nHEAP --------------------- END\n"

    def __len__(self):
        return len(self.array)

    def update_f_value(self, item, new_f):
        for i in self.array:
            if i[2] == item:
                i[0] = new_f

        heapq.heapify(self.array)










#!/usr/bin/env python3

import os
import numpy as np


class Data:
    """Represents a single piece of data."""
    def __init__(self, data, width, height):
        self.w, self.h = width, height

        self.pixels = np.array(data)

    def get_pixel(self, r, c):
        return self.pixels[r][c]

    def __str__(self):
        rows = []
        for r in self.pixels:
            rows.append("".join(r))
        return "\n".join(rows)

    def ascii_to_int(c):
        if c == ' ':
            return 0
        elif c == '+':
            return 1
        elif c == '#':
            return 2

    def int_to_ascii(c):
        if c == 0:
            return ' '
        elif c == 1:
            return '+'
        elif c == 2:
            return '#'

class Dataset:
    def __init__(self, n, item_dimens):
        self.data = []
        self.width, self.height = item_dimens
        self.size = n

    def load_data(self, filename):
        """Reads n image from file and return list of Data objects."""
        fin = self.read(filename)
        fin.reverse()
        for i in range(self.size):
            data = []
            for j in range(self.height):
                data.append(list(fin.pop()))
            if len(data[0]) < self.width - 1:
                # eof
                print("Finished reading {} objects.".format(n))
                break
            self.data.append(Data(data, self.width, self.height))

    def read(self, filename):
        if os.path.exists(filename):
            return [_[:-1] for _ in open(filename).readlines()]

    def __getitem__(self, idx):
        return self.data[idx]

if __name__ == "__main__":
    
    d = Dataset(2, (28, 28)) 
    d.load_data("data/digitdata/trainingimages")

    for data in d:
        print(data)
        print("=" * 50)
    


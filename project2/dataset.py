#!/usr/bin/env python3

import os
import numpy as np


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
        self.data, self.labels = [], []
        self.width, self.height = item_dimens
        self.size = n

    def load_data(self, filename):
        """Reads n image from file and return list of Data objects."""
        fin = self.read(filename)
        fin.reverse()
        for i in range(self.size):
            data = []
            for j in range(self.height):
                row  = list(fin.pop())
                int_row = np.array(list(map(ascii_to_int, row)))
                data.append(int_row)
            if len(data[0]) < self.width - 1:
                # eof
                print("Finished reading {} objects.".format(n))
                break
            self.data.append(np.array(data))
        self.data = np.array(self.data)
        return self.data

    def load_labels(self, filename):
        """Loads labels from file"""
        fin = self.read(filename)
        for l in fin[:min(self.size, len(fin))]:
            if l == '': break
            self.labels.append(int(l))
        self.labels = np.array(self.labels)
        return self.labels

    def read(self, filename):
        if os.path.exists(filename):
            return [_[:-1] for _ in open(filename).readlines()]

    def get_data(self):
        return self.data

    def get_labels(self):
        return self.labels

    def get_labeled_data(self):
        return list(zip(self.data, self.labels))

    def __getitem__(self, idx):
        """Returns a tuple with data object and corresponding label"""
        return (self.data[idx], self.labels[idx])

    def __len__(self):
        return len(self.data)

    def shape(self):
        return (self.width, self.height)

if __name__ == "__main__":
    
    d = Dataset(2, (28, 28)) 
    d.load_data("data/digitdata/trainingimages")
    d.load_labels("data/digitdata/traininglabels")
    for (data, label) in d:
        print(data)
        print("Label: ", label)
        print("=" * 50)

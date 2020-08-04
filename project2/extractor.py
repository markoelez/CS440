#!/usr/bin/env python3

from dataset import Dataset


DIGIT_WIDTH = 28
DIGIT_HEIGHT = 28

def get_features(datum):
    pixels = datum.get_pixels()
    features = {}
    for x in range(DIGIT_WIDTH):
        for y in range(DIGIT_HEIGHT):
            if datum.get_pixel(x, y) > 0:
                features[(x, y)] = 1
            else:
                features[(x, y)] = 0
    return features


if __name__ == "__main__":

    d = Dataset(2, (28, 28)) 
    d.load_data("data/digitdata/trainingimages")
    d.load_labels("data/digitdata/traininglabels")

    data = d.get_data()
    for x in data:
        print(get_features(x))
        print("=" * 80)

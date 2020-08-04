#!/usr/bin/env python3

import sys
import argparse
from perceptron import PerceptronClassifier
from dataset import Dataset


def print_break():
    """Utility for formatting output"""
    print("=" * 60)

if __name__ == "__main__":
    print("=" * 60)
    print("=" * 60)
    parser = argparse.ArgumentParser(description="Run a suite of classification algorithms on the provided dataset.")
    parser.print_help()
    print("=" * 60)
    print("=" * 60)
    parser.add_argument('-c', '--classifier', type=str, help='Choose which classifier to use', default='perceptron')
    parser.add_argument('-d', '--dataset', type=str, help='digit or faces', default='digit')
    parser.add_argument('-v', '--verbose', help='Set flag for verbose output', action='store_true')
    parser.add_argument('-e', '--epochs', type=int, help='Number of training epochs to use', default=1)
    parser.add_argument('-s', '--split', type=int, help='Validation split for train/test data', default=0.1)
    args = parser.parse_args()
    print(args)
    print()

    if args.classifier == 'perceptron':
        n = 100

        if args.dataset == 'digit':
            datum_shape = (28, 28)

            # load training data
            td = Dataset(n, datum_shape)
            td.load_data("data/digitdata/trainingimages")
            td.load_labels("data/digitdata/traininglabels")

            # load validation data
            vd = Dataset(n, datum_shape)
            vd.load_data("data/digitdata/validationimages")
            vd.load_labels("data/digitdata/validationlabels")

            # load testing data
            fd = Dataset(n, datum_shape)
            fd.load_data("data/digitdata/testimages")
            fd.load_labels("data/digitdata/testlabels")

            model = PerceptronClassifier(datum_shape, 10, bool(args.verbose))
            
            print("Training...\n")
            model.train(td.get_data(), td.get_labels(), args.epochs, args.split)
            print_break()

            # validate
            print("Validing model...\n")
            model.evaluate(fd.get_data(), fd.get_labels())
            print_break()

            # test
            print("Testing model...\n")
            model.evaluate(fd.get_data(), fd.get_labels())
            print_break()

        else:
            datum_shape = (60, 70)

            # load training data
            td = Dataset(n, datum_shape)
            td.load_data("data/facedata/facedatatrain")
            td.load_labels("data/facedata/facedatatrainlabels")

            # load validation data
            vd = Dataset(n, datum_shape)
            vd.load_data("data/facedata/facedatavalidation")
            vd.load_labels("data/facedata/facedatavalidationlabels")

            # load testing data
            fd = Dataset(n, datum_shape)
            fd.load_data("data/facedata/facedatatest")
            fd.load_labels("data/facedata/facedatatestlabels")

            model = PerceptronClassifier(datum_shape, 2, bool(args.verbose))
            
            print("Training...\n")
            model.train(td.get_data(), td.get_labels(), args.epochs, args.split)
            print_break()

            # validate
            print("Validing model...\n")
            model.evaluate(fd.get_data(), fd.get_labels())
            print_break()

            # test
            print("Testing model...\n")
            model.evaluate(fd.get_data(), fd.get_labels())
            print_break()

    else:
        # TODO
        pass


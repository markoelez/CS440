#!/usr/bin/env python3

import sys 
import numpy as np
from dataset import Dataset
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score


def activation(x):
    return 1 / (1 + np.exp(-x))

def cost_function(y_true, y_pred):
    """Mean squared error cost function"""
    return np.sum((y_true - y_pred) ** 2)


class PerceptronClassifier:

    def __init__(self, input_dim, n_classes, seed=99):
        self.seed = seed
        np.random.seed(self.seed)

        self.n_class = n_classes
        
        # weights shape: (9, 28, 28)
        self.weights = np.random.randn(n_classes, input_dim, input_dim)

    def train(self, X, y, epochs, validation_split=0.2):
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=validation_split)

        for e in range(epochs):
            x_train, y_train = shuffle(x_train, y_train)
            
            for x, y in zip(x_train, y_train):
                pred = self.predict(x)
                print("Predicted {}. Expected {}. Correct? {}\n".format(pred, y, pred == y))
                if pred != y:
                    # update weights
                    self.weights[y] = self.weights[y] + x 
                    self.weights[pred] = self.weights[pred] - x 

            # test 
            total = len(y_test)
            correct = 0
            for x, y in zip(x_test, y_test):
                pred = self.predict(x)
                if pred == y: correct += 1

            print("=" * 60)
            print("Finished epoch {} with accuracy {}".format(e, correct/total))
            print("=" * 60)

    def evaluate(self, X, Y):
        correct  = 0
        for x, y in zip(X, Y):
            pred = self.predict(x)
            if pred == y: correct += 1
        perc = correct / len(Y) 
        print("\nDone. {} correct out of {}: {}% \n".format(correct, len(Y), perc * 100))
    
    def predict(self, a):
        """Make a prediction based on the current state of the perceptron"""
        g = []
        for w in self.weights:
            z = np.dot(w.reshape(w.shape[0] * w.shape[1], ), a.reshape(a.shape[0] * a.shape[1], ).T)
            g.append(z)
        return np.argmax(g)


if __name__ == "__main__":

    d = Dataset(50, (28, 28)) 
    d.load_data("data/digitdata/trainingimages")
    d.load_labels("data/digitdata/traininglabels")

    model = PerceptronClassifier(d.shape()[1], 10)

    model.train(d.get_data(), d.get_labels(), 2, 0.1)

    model.evaluate(d.get_data(), d.get_labels())


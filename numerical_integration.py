from math import *

class NumericalIntegration:
    def __init__(self, fun, n):
        self.fun = fun
        self.n = n
        self.points = []
        self.weights = []
        match self.n:
            case 2:
                self.points = [
                    -sqrt(1/3),
                    sqrt(1/3)
                ]
                self.weights = [
                    1,
                    1
                ]
            case 3:
                self.points = [
                    -sqrt(3/5),
                    0,
                    sqrt(3/5)
                ]
                self.weights = [
                    5/9,
                    8/9,
                    5/9
                ]
            case 4:
                self.points = [
                    -sqrt(3/7 - 2/7*sqrt(6/5)),
                    -sqrt(3/7 +2/7*sqrt(6/5)),
                    sqrt(3/7 +2/7*sqrt(6/5)),
                    sqrt(3/7 - 2/7*sqrt(6/5)),
                ]
                self.weights = [
                    (18+sqrt(30))/36,
                    (18-sqrt(30))/36,
                    (18-sqrt(30))/36,
                    (18+sqrt(30))/36
                ]

    def calculate1d(self):
        result = 0
        for i in range (0, self.n):
            x = self.points[i]
            result += self.weights[i] * self.fun(x)
        return result
    
    def calculate2d(self):
        result = 0
        for i in range (0, self.n):
            x = self.points[i]
            for j in range (self.n):
                y = self.points[j]
                result += self.weights[i] * self.weights[j] * self.fun(x, y)
        return result
from common import *
from math import *

class GaussianQuadrature:
    '''
    A class for numerical integration using Gaussian Quadrature.
    
    fun:        function to integrate
    n:          number of integration points
    points:     list of integration points, xi
    weights:    weights for integration points, wi
    '''
    def __init__(self, n: int, fun):
        self.fun = fun
        self.n: int = n
        self.points: list[float] = []
        self.weights: list[float] = []
        self.initPointsAndWeights()

    def initPointsAndWeights(self) -> None:
        '''
        Initializes lists containing integration points and their weights.
        '''
        match self.n:
            case 1:
                self.points = [0]
                self.weights = [2]
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
                    -sqrt(3/7 + 2/7*sqrt(6/5)),
                    -sqrt(3/7 - 2/7*sqrt(6/5)),
                    sqrt(3/7 - 2/7*sqrt(6/5)),
                    sqrt(3/7 + 2/7*sqrt(6/5))
                ]
                self.weights = [
                    
                    (18 - sqrt(30))/36,
                    (18 + sqrt(30))/36,
                    (18 + sqrt(30))/36,
                    (18 - sqrt(30))/36
                ]
            case 5:
                self.points = [
                    -(1/3)*sqrt(5 + 2*sqrt(10/7)),
                    -(1/3)*sqrt(5 - 2*sqrt(10/7)),
                    0,
                    (1/3)*sqrt(5 - 2*sqrt(10/7)),
                    (1/3)*sqrt(5 + 2*sqrt(10/7))
                ]
                self.weights = [
                    (322 - 13*sqrt(70))/900,
                    (322 + 13*sqrt(70))/900,
                    128/225,
                    (322 + 13*sqrt(70))/900,
                    (322 - 13*sqrt(70))/900
                ]
            case _:
                raise FiniteElementMethodException('Number of nodes in numerical integration (n) must be an integer in range (1;5).')      

    def calculateIntegral1d(self) -> float:
        '''
        Calculates integral for function of 1 variable f(x).
        '''
        result = 0.0
        for i in range (0, self.n):
            x = self.points[i]
            result += self.weights[i] * self.fun(x)
        return result
    
    def calculateIntegral2d(self) -> float:
        '''
        Calculates integral for function of 2 variables f(x, y).
        '''
        result = 0.0
        for i in range (0, self.n):
            x = self.points[i]
            for j in range (self.n):
                y = self.points[j]
                result += self.weights[i] * self.weights[j] * self.fun(x, y)
        return result
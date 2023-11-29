from grid import *
import numpy as np
from numpy import linalg
from numpy._typing import NDArray

class SystemOfEquations():
    '''
    Class for calculating temperature in each node of the grid by creating and solving a system of equations.

    H:      global matrix of H + Hbc od each element of the grid
    P:      global P vector
    dim:    dimensions of H matrix and P vector 
    '''
    def __init__(self, grid: Grid):
        self.dim = grid.globalData.nodesNumber
        self.H = np.zeros((self.dim, self.dim))
        self.P = np.zeros((self.dim, 1))
        self.aggregateH(grid)
        self.aggreagteP(grid)

    def aggregateH(self, grid: Grid) -> None:
        '''
        Creates global H matrix from local (per element) matrices H and Hbc.
        '''
        for element in grid.elements:
            localH = element.H + element.Hbc
            for j in range(0, 4):
                for i in range(0, 4):
                    self.H[element.IDs[j] - 1][element.IDs[i] - 1] += localH[j][i]
        print(self.H)

    def aggreagteP(self, grid: Grid) -> None:
        '''
        Creates global P vector from local (per element) P vectors.
        '''
        for element in grid.elements:
            for i in range(0, 4):
                self.P[element.IDs[i] - 1] += element.P[i]
        print(self.P)

    def solve(self) -> NDArray:
        '''
        Solves system of equations created form H matrix and P vector.
        H[0] = P[0]
        H[1] = P[1]
        ...
        H[n] = P[n]
        '''
        result = linalg.solve(self.H, self.P)
        print(result)
        return result
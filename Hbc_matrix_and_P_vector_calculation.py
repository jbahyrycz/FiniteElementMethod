from grid import *
import numpy as np

class HbcMatrixAndPVectorCalculation():
    '''
    Calculations of Hbc matrix and P vector for each element of the given grid.
    '''
    def __init__(self):
        raise MyException("HbcMatrixAndPVectorCalculation is an abstract class, you cannot create an instance of this class.")
    
    @staticmethod
    def calculate(n: int, grid: Grid) -> None:
        '''
        Calculates Hbc matrices and P vectors for each element in the grid, output is stored in Element.Hbc and Elemeny.P.
        '''
        uEl = UniversalElement(n)
        for element in grid.elements:
            element.Hbc, element.P = HbcMatrixAndPVectorCalculation.calculateForElement([grid.nodes[element.IDs[0] - 1], 
                                                                grid.nodes[element.IDs[1] - 1],
                                                                grid.nodes[element.IDs[2] - 1],
                                                                grid.nodes[element.IDs[3] - 1]],
                                                                uEl, grid.globalData)
            print(f"Hbc:\n{element.Hbc}\nP:\n{element.P}")

    @staticmethod
    def calculateForElement(nodes: list[Node], uEl: UniversalElement, glData: GlobalData) -> None:
        '''
        Calculates Hbc matrix and P vector for the element.
        '''
        Hbc = np.zeros((4, 4))
        P = np.zeros((4, 1))
        tempList = []
        tempList.append(HbcMatrixAndPVectorCalculation.calculateForSurface(uEl.surfaces[0], (nodes[0], nodes[1]), uEl.weights, uEl.n, glData.alfa, glData.tot))
        tempList.append(HbcMatrixAndPVectorCalculation.calculateForSurface(uEl.surfaces[1], (nodes[1], nodes[2]), uEl.weights, uEl.n, glData.alfa, glData.tot))
        tempList.append(HbcMatrixAndPVectorCalculation.calculateForSurface(uEl.surfaces[2], (nodes[2], nodes[3]), uEl.weights, uEl.n, glData.alfa, glData.tot))
        tempList.append(HbcMatrixAndPVectorCalculation.calculateForSurface(uEl.surfaces[3], (nodes[3], nodes[0]), uEl.weights, uEl.n, glData.alfa, glData.tot))
        for surfaceHbc, surfaceP in tempList:
            Hbc+=surfaceHbc
            P+=surfaceP
        return Hbc, P
    
    @staticmethod
    def calculateForSurface(surface: Surface, nodes: tuple[Node], weights: list[float], n: int, alfa: int, tot: int) -> tuple:
        '''
        Calculates Hbc matrix and P vector for the given surface of the element.
        '''
        Hbc = np.zeros((4, 4))
        P = np.zeros((4, 1))
        if nodes[0].BC == 0 or nodes[1].BC == 0:
            return Hbc, P
        L = sqrt(pow(nodes[0].x-nodes[1].x, 2)+pow(nodes[0].y-nodes[1].y, 2))
        detJ = L/2
        for i in range(0, n):
            mx = np.array([[surface.N[i][0]],
                            [surface.N[i][1]],
                            [surface.N[i][2]],
                            [surface.N[i][3]]])
            Hbc += np.matmul(mx, mx.transpose())*weights[i]
            P += mx*weights[i]
        Hbc = Hbc*alfa*detJ
        P = P*alfa*tot*detJ
        return Hbc, P
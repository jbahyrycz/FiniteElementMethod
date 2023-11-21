from grid import *
import numpy as np

class HbcMatrixCalculation():
    '''
    Calculations of Hbc matrix for each element of the given grid.
    '''
    def __init__(self):
        raise MyException("HbcMatrixCalculation is an abstract class, you cannot create an instance of this class.")
    
    @staticmethod
    def calculateHbcMatrices(n: int, grid: Grid) -> None:
        '''
        Calculates Hbc matrices for each element in the grid, output is stored in Element.Hbc.
        '''
        uEl = UniversalElement(n)
        for element in grid.elements:
            element.Hbc = HbcMatrixCalculation.calculateHbcMatrix([grid.nodes[element.IDs[0] - 1], 
                                                                grid.nodes[element.IDs[1] - 1],
                                                                grid.nodes[element.IDs[2] - 1],
                                                                grid.nodes[element.IDs[3] - 1]],
                                                                uEl, grid.globalData)
            print(element.Hbc)

    @staticmethod
    def calculateHbcMatrix(nodes: list[Node], uEl: UniversalElement, glData: GlobalData) -> None:
        '''
        Calculates Hbc matrix for the element.
        '''
        HbcList = []
        HbcList.append(HbcMatrixCalculation.calculateMatrixForSurface(uEl.surfaces[0], (nodes[0], nodes[1]), uEl.weights, uEl.n, glData.alfa))
        HbcList.append(HbcMatrixCalculation.calculateMatrixForSurface(uEl.surfaces[1], (nodes[1], nodes[2]), uEl.weights, uEl.n, glData.alfa))
        HbcList.append(HbcMatrixCalculation.calculateMatrixForSurface(uEl.surfaces[2], (nodes[2], nodes[3]), uEl.weights, uEl.n, glData.alfa))
        HbcList.append(HbcMatrixCalculation.calculateMatrixForSurface(uEl.surfaces[3], (nodes[3], nodes[0]), uEl.weights, uEl.n, glData.alfa))
        #for element in HbcList: print(element)
        Hbc = sum(HbcList)
        return Hbc
    
    @staticmethod
    def calculateMatrixForSurface(surface: Surface, nodes: tuple[Node], weights: list[float], n: int, alfa: int):
        '''
        Calculates Hbc matrix for the given surface of the element.
        '''
        Hbc = np.zeros((4, 4))
        if nodes[0].BC == 0 or nodes[1].BC == 0:
            return Hbc
        for i in range(0, n):
            L = sqrt(pow(nodes[0].x-nodes[1].x, 2)+pow(nodes[0].y-nodes[1].y, 2))
            detJ = L/2
            mx = np.array([[surface.N[i][0]],
                            [surface.N[i][1]],
                            [surface.N[i][2]],
                            [surface.N[i][3]]])
            Hbc+=alfa*np.matmul(mx, mx.transpose())*weights[i]
        Hbc = Hbc*detJ
        return Hbc
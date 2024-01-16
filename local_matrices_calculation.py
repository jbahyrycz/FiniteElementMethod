from common import *
from universal_element import UniversalElement, Surface
from grid import Grid, GlobalData, Node
from math import *
import numpy as np

class LocalMatricesCalculation:
    '''
    Abstract class for calculating of H, C, Hbc matrices and P vector for each element of the given grid.
    '''
    def __init__(self):
        raise FiniteElementMethodException('LocalMatricesCalculation is an abstract class, you cannot create an instance of this class.')
    
    @staticmethod
    def calculate(n: int, grid: Grid) -> None:
        '''
        Calculates H, C, Hbc matrices and P vector for each element in the grid, output is stored in Element class.
        '''
        uEl = UniversalElement(n)
        for element in grid.elements:
            element.H, element.C, element.Hbc, element.P = LocalMatricesCalculation._calculateForElement([grid.nodes[element.nodeIds[0] - 1],
                                      grid.nodes[element.nodeIds[1] - 1],
                                      grid.nodes[element.nodeIds[2] - 1],
                                      grid.nodes[element.nodeIds[3] - 1]],
                                      uEl, grid.globalData)
            #print(f'H:\n{element.H}\nC:{element.C}\nHbc:\n{element.Hbc}\nP:\n{element.P}')

    @staticmethod
    def _calculateForElement(nodes: list[Node], uEl: UniversalElement, glData: GlobalData) -> None:
        '''
        Calculates H, C, Hbc marices and P vector for the element.
        '''
        xCoords, yCoords = LocalMatricesCalculation._fillXYCoords(nodes)
        dXdKsiTab, dXdEtaTab, dYdKsiTab, dYdEtaTab = LocalMatricesCalculation._fillXYKsiEtaTabs(xCoords, yCoords, uEl)
        dNdXTab, dNdYTab, detTab = LocalMatricesCalculation._dNdXdNdY(dXdKsiTab, dXdEtaTab, dYdKsiTab, dYdEtaTab, uEl)
        ipHMatrices, ipCMatrices = LocalMatricesCalculation._calculateForIntegrationPoints(dNdXTab, dNdYTab, uEl.NTab, detTab, uEl.n, glData.conductivity, glData.density, glData.specificHeat)
        
        H = np.zeros((4, 4))
        C = np.zeros((4, 4))
        Hbc = np.zeros((4, 4))
        P = np.zeros((4, 1))

        for i in range(0, uEl.n*uEl.n):
            H += ipHMatrices[i]*(uEl.weights[i//uEl.n])*(uEl.weights[i%uEl.n])
            C += ipCMatrices[i]*(uEl.weights[i//uEl.n])*(uEl.weights[i%uEl.n])

        tempList = []
        tempList.append(LocalMatricesCalculation._calculateForSurface(uEl.surfaces[0], (nodes[0], nodes[1]), uEl.weights, uEl.n, glData.alfa, glData.tot))
        tempList.append(LocalMatricesCalculation._calculateForSurface(uEl.surfaces[1], (nodes[1], nodes[2]), uEl.weights, uEl.n, glData.alfa, glData.tot))
        tempList.append(LocalMatricesCalculation._calculateForSurface(uEl.surfaces[2], (nodes[2], nodes[3]), uEl.weights, uEl.n, glData.alfa, glData.tot))
        tempList.append(LocalMatricesCalculation._calculateForSurface(uEl.surfaces[3], (nodes[3], nodes[0]), uEl.weights, uEl.n, glData.alfa, glData.tot))
        for surfaceHbc, surfaceP in tempList:
            Hbc+=surfaceHbc
            P+=surfaceP
        return H, C, Hbc, P
    
    @staticmethod
    def _fillXYCoords(nodes: list[Node]) -> tuple[list[float]]:
        '''
        Fills lists storing x and y coords of nodes belonging to the element.
        '''
        xCoords = []; yCoords = []
        for i in range(0, 4):
            xCoords.append(nodes[i].x)
            yCoords.append(nodes[i].y)
        #print(f'xCoords: {xCoords}\nyCoords: {yCoords}')
        return xCoords, yCoords
    
    @staticmethod
    def _fillXYKsiEtaTabs(xCoords: list[float], yCoords: list[float], uEl: UniversalElement) -> tuple[list[float]]:
        '''
        Calculates dx/dksi, dx/deta, dy/dksi, dy/deta for every integration point and returns 4 tables with output.
        '''
        dXdKsiTab = []; dXdEtaTab = []; dYdKsiTab = []; dYdEtaTab = []
        for i in range(0, uEl.n*uEl.n):
            dXdKsiTab.append(LocalMatricesCalculation._interpolate(uEl.dNdKsiTab[i][0], uEl.dNdKsiTab[i][1], uEl.dNdKsiTab[i][2], uEl.dNdKsiTab[i][3], xCoords))
            dXdEtaTab.append(LocalMatricesCalculation._interpolate(uEl.dNdEtaTab[i][0], uEl.dNdEtaTab[i][1], uEl.dNdEtaTab[i][2], uEl.dNdEtaTab[i][3], xCoords))
            dYdKsiTab.append(LocalMatricesCalculation._interpolate(uEl.dNdKsiTab[i][0], uEl.dNdKsiTab[i][1], uEl.dNdKsiTab[i][2], uEl.dNdKsiTab[i][3], yCoords))
            dYdEtaTab.append(LocalMatricesCalculation._interpolate(uEl.dNdEtaTab[i][0], uEl.dNdEtaTab[i][1], uEl.dNdEtaTab[i][2], uEl.dNdEtaTab[i][3], yCoords))
        #print(f'dXdKsiTab: {dXdKsiTab}\ndXdEtaTab: {dXdEtaTab}\ndYdKsiTab: {dYdKsiTab}\ndYdEtaTab: {dYdEtaTab}')
        return dXdKsiTab, dXdEtaTab, dYdKsiTab, dYdEtaTab
    
    @staticmethod
    def _dNdXdNdY(dXdKsiTab: list, dXdEtaTab: list, dYdKsiTab: list, dYdEtaTab: list, uEl: UniversalElement) -> tuple[list[float]]:
        '''
        Fills dN/dx and dN/dy tables and calculates Jacobian and det[J].

        mxJ: Jacobian matrix
        detJ: Jacobian determinant
        '''
        def initialize_dNdXdNdY(n: int) -> tuple[list[list]]:
            '''
            Initializes empty tables for dN/dx and dN/dy calculations.
            '''
            dNdXTab = []; dNdYTab = []
            for j in range(n*n):
                dNdXTab.append([])
                dNdYTab.append([])
                for i in range (0, 4):
                    dNdXTab[j].append(0)
                    dNdYTab[j].append(0)
            return dNdXTab, dNdYTab
    
        dNdXTab, dNdYTab = initialize_dNdXdNdY(uEl.n)
        detTab = []
        for j in range(uEl.n*uEl.n):
            mxJ = np.array([[dXdKsiTab[j], dYdKsiTab[j]],
                             [dXdEtaTab[j], dYdEtaTab[j]]])
            #print(f'Jacobian matrix:\n{mxJ}')
            detJ = np.linalg.det(mxJ)
            #print(f'Jacobian determinant:\n{detJ}')
            detTab.append(detJ)
            mx1 = np.array([[dYdEtaTab[j], -dYdKsiTab[j]],
                             [-dXdEtaTab[j], dXdKsiTab[j]]])
            for i in range (0, 4):
                mx2 = np.array([[uEl.dNdKsiTab[j][i]],[uEl.dNdEtaTab[j][i]]])
                # (1/detJ)*mx1 = mxJ^(-1)
                mxOutput = np.matmul(((1/detJ)*mx1), mx2)
                dNdXTab[j][i] = mxOutput[0][0]
                dNdYTab[j][i] = mxOutput[1][0]
        #print('dNdXTab:')
        #print2dTab(dNdXTab)
        #print('dNdYTab:')
        #print2dTab(dNdYTab)
        return dNdXTab, dNdYTab, detTab

    @staticmethod
    def _calculateForIntegrationPoints(dNdXTab: list, dNdYTab: list, NTab: list, detTab: list, n: int, c: int, d: int, sH: int) -> tuple[np.ndarray]:
        '''
        Calculates H, C matrices for each integration point. Returns list of matrices.
        '''
        mxHTab = []
        mxCTab = []
        for i in range(0, n*n):
            mxDNdX = np.array([[dNdXTab[i][0]],
                             [dNdXTab[i][1]],
                             [dNdXTab[i][2]],
                             [dNdXTab[i][3]]])
            mxDNdY = np.array([[dNdYTab[i][0]],
                             [dNdYTab[i][1]],
                             [dNdYTab[i][2]],
                             [dNdYTab[i][3]]])
            mxN = np.array([[NTab[i][0]],
                             [NTab[i][1]],
                             [NTab[i][2]],
                             [NTab[i][3]]])
            ipMxH = c*(np.matmul(mxDNdX, mxDNdX.transpose()) + np.matmul(mxDNdY, mxDNdY.transpose()))*detTab[i]
            ipMxC = sH*d*(np.matmul(mxN, mxN.transpose()))*detTab[i]
            #print(f'IP {i+1}:\n{ipMxH}')
            mxHTab.append(ipMxH)
            mxCTab.append(ipMxC)
        return mxHTab, mxCTab
    
    @staticmethod
    def _calculateForSurface(surface: Surface, nodes: tuple[Node], weights: list[float], n: int, alfa: int, tot: int) -> tuple:
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
    
    @staticmethod
    def _interpolate(dN1: float, dN2: float, dN3: float, dN4: float, var: list[float]) -> float:
        '''
        Returns dx/deta, dx/dksi, dy/deta or dy/dksi depending on given arguments.
        '''
        return dN1*var[0] + dN2*var[1] + dN3*var[2] + dN4*var[3]
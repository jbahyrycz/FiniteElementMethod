from grid import *
import numpy as np
class HMatrixCalculation():
    @staticmethod
    def calculateHMatrices(n: int, grid: Grid) -> None:
        '''
        Calculates H matrices for each element in the grid, output is stored in Element.Hmatrix.
        '''
        uEl = UniversalElement(n)
        for element in grid.elements:
            element.H = HMatrixCalculation.calculateHMatrix([grid.nodes[element.IDs[0] - 1],
                                      grid.nodes[element.IDs[1] - 1],
                                      grid.nodes[element.IDs[2] - 1],
                                      grid.nodes[element.IDs[3] - 1]],
                                      uEl, grid.globalData)
            print(element.H)

    @staticmethod
    def calculateHMatrix(nodes: list[Node], uEl: UniversalElement, glData: GlobalData) -> None:
        '''
        Calculates H matrix for the element.
        '''
        xCoords, yCoords = HMatrixCalculation.fillXYCoords(nodes)
        dXdKsiTab, dXdEtaTab, dYdKsiTab, dYdEtaTab = HMatrixCalculation.fillXYKsiEtaTabs(xCoords, yCoords, uEl)
        dNdXTab, dNdYTab, detTab = HMatrixCalculation.fillDNdXdNdYTabs(dXdKsiTab, dXdEtaTab, dYdKsiTab, dYdEtaTab, uEl)
        ipHMatrices = HMatrixCalculation.calculateHMatrixForIntegrationPoints(dNdXTab, dNdYTab, detTab, uEl.n, glData.conductivity)
        
        H = np.zeros((4, 4))
        for i in range(0, uEl.n*uEl.n):
            #print(ipHMatrices[i])
            H += ipHMatrices[i]*(uEl.weights[i//uEl.n])*(uEl.weights[i%uEl.n])
        return H
    
    @staticmethod
    def fillXYCoords(nodes: list[Node]) -> tuple[float]:
        '''
        Fills lists storing x and y coords of nodes belonging to the element.
        '''
        xCoords = []; yCoords = []
        for i in range(0, 4):
            xCoords.append(nodes[i].x)
            yCoords.append(nodes[i].y)
        #print(f"xCoords: {xCoords}\nyCoords: {yCoords}")
        return xCoords, yCoords
    
    @staticmethod
    def fillXYKsiEtaTabs(xCoords: list[float], yCoords: list[float], uEl: UniversalElement) -> tuple[list[float]]:
        '''
        Calculates dx/dksi, dx/deta, dy/dksi, dy/deta for every integration point and returns 4 tables with output.
        '''
        dXdKsiTab = []; dXdEtaTab = []; dYdKsiTab = []; dYdEtaTab = []
        for i in range(0, uEl.n*uEl.n):
            dXdKsiTab.append(HMatrixCalculation.dKsi(uEl.dNdKsiTab[i][0], uEl.dNdKsiTab[i][1], uEl.dNdKsiTab[i][2], uEl.dNdKsiTab[i][3], xCoords))
            dXdEtaTab.append(HMatrixCalculation.dEta(uEl.dNdEtaTab[i][0], uEl.dNdEtaTab[i][1], uEl.dNdEtaTab[i][2], uEl.dNdEtaTab[i][3], xCoords))
            dYdKsiTab.append(HMatrixCalculation.dKsi(uEl.dNdKsiTab[i][0], uEl.dNdKsiTab[i][1], uEl.dNdKsiTab[i][2], uEl.dNdKsiTab[i][3], yCoords))
            dYdEtaTab.append(HMatrixCalculation.dKsi(uEl.dNdEtaTab[i][0], uEl.dNdEtaTab[i][1], uEl.dNdEtaTab[i][2], uEl.dNdEtaTab[i][3], yCoords))
        #print(f"dXdKsiTab: {dXdKsiTab}\ndXdEtaTab: {dXdEtaTab}\ndYdKsiTab: {dYdKsiTab}\ndYdEtaTab: {dYdEtaTab}")
        return dXdKsiTab, dXdEtaTab, dYdKsiTab, dYdEtaTab
    
    @staticmethod
    def fillDNdXdNdYTabs(dXdKsiTab: list, dXdEtaTab: list, dYdKsiTab: list, dYdEtaTab: list, uEl: UniversalElement) -> tuple[list[float]]:
        '''
        Fills dN/dx and dN/dy tables and calculates Jacobian and det[J].

        mxJ: Jacobian matrix
        detJ: Jacobian determinant
        '''
        dNdXTab, dNdYTab = HMatrixCalculation.initializeDNdXdNdYTabs(uEl.n)
        detTab = []
        for j in range(uEl.n*uEl.n):
            mxJ = np.array([[dXdKsiTab[j], dYdKsiTab[j]],
                             [dXdEtaTab[j], dYdEtaTab[j]]])
            #print(f"Jacobian matrix:\n{mxJ}")
            detJ = np.linalg.det(mxJ)
            #print(f"Jacobian determinant:\n{detJ}")
            detTab.append(detJ)
            mx1 = np.array([[dYdEtaTab[j], -dYdKsiTab[j]],
                             [-dXdEtaTab[j], dXdKsiTab[j]]])
            for i in range (0, 4):
                mx2 = np.array([[uEl.dNdKsiTab[j][i]],[uEl.dNdEtaTab[j][i]]])
                # (1/detJ)*mx1 = mxJ^(-1)
                mxOutput = np.matmul(((1/detJ)*mx1), mx2)
                dNdXTab[j][i] = mxOutput[0][0]
                dNdYTab[j][i] = mxOutput[1][0]
        #print("dNdXTab:")
        #print2dTab(dNdXTab)
        #print("dNdYTab:")
        #print2dTab(dNdYTab)
        return dNdXTab, dNdYTab, detTab
    
    @staticmethod
    def initializeDNdXdNdYTabs(n: int) -> tuple[list[list]]:
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

    @staticmethod
    def calculateHMatrixForIntegrationPoints(dNdXTab: list, dNdYTab: list, detTab: list, n: int, k: int) -> list[np.ndarray]:
        '''
        Calculates H matrix for each integration point. Returns list of matrixes.
        '''
        mxHTab = []
        for i in range(0, n*n):
            mxDNdX = np.array([[dNdXTab[i][0]],
                             [dNdXTab[i][1]],
                             [dNdXTab[i][2]],
                             [dNdXTab[i][3]]])
            mxDNdY = np.array([[dNdYTab[i][0]],
                             [dNdYTab[i][1]],
                             [dNdYTab[i][2]],
                             [dNdYTab[i][3]]])
            ipMxH = k*(np.matmul(mxDNdX, mxDNdX.transpose()) + np.matmul(mxDNdY, mxDNdY.transpose()))*detTab[i]
            #print(f"IP {i+1}:\n{ipMxH}")
            mxHTab.append(ipMxH)
        return mxHTab

    @staticmethod
    def dKsi(dN1dKsi: float,
                     dN2dKsi: float,
                     dN3dKsi: float,
                     dN4dKsi: float,
                     var: float) -> float:
        '''
        Returns dx/dksi or dy/dksi depending on the argument given.
        '''
        return dN1dKsi*var[0] + dN2dKsi*var[1] + dN3dKsi*var[2] + dN4dKsi*var[3]

    @staticmethod
    def dEta(dN1dEta: float,
                     dN2dEta: float,
                     dN3dEta: float,
                     dN4dEta: float,
                     var: float) -> float:
        '''
        Returns dx/deta or dy/deta depending on the argument given.
        '''
        return dN1dEta*var[0] + dN2dEta*var[1] + dN3dEta*var[2] + dN4dEta*var[3]
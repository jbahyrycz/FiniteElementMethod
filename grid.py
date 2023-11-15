from common import *
from universal_element import *
import numpy as np

class GlobalData:
    '''
    Stores general information like simulation time, conductivity, initial temperature, density etc.
    '''
    def __init__(self, globalDataDict: dict):
        self.simulationTime = globalDataDict["SimulationTime"]
        self.simulationStepTime = globalDataDict["SimulationStepTime"]
        self.conductivity = globalDataDict["Conductivity"]
        self.alfa = globalDataDict["Alfa"]
        self.tot = globalDataDict["Tot"]
        self.initialTemp = globalDataDict["InitialTemp"]
        self.density = globalDataDict["Density"]
        self.specificHeat = globalDataDict["SpecificHeat"]
        self.nodesNumber = globalDataDict["Nodesnumber"]
        self.elementsNumber = globalDataDict["Elementsnumber"]

    def print(self) -> None:
        print(f"Simulation time: \t{self.simulationTime}")
        print(f"Simulation step time: \t{self.simulationStepTime}")
        print(f"Conductivity: \t\t{self.conductivity}")
        print(f"Alfa: \t\t\t{self.alfa}")
        print(f"Tot: \t\t\t{self.tot}")
        print(f"Initial temp: \t\t{self.initialTemp}")
        print(f"Density: \t\t{self.density}")
        print(f"Specific heat: \t\t{self.specificHeat}")
        print(f"Nodes number: \t\t{self.nodesNumber}")
        print(f"Elements number: \t{self.elementsNumber}")

class Node:
    '''
    Stores information about a single node of the grid.

    id:      Node's ID
    x:       x coord
    y:       y coord
    '''
    def __init__(self, id: int, x: float, y: float):
        self.id = id
        self.x = x
        self.y = y

    def print(self) -> None:
        print(f"Node {self.id}: \t({self.x}, {self.y})")

class Element:
    '''
    Stores information about a single 4-node element of the grid.

    id:         Element's ID
    IDs:        IDs od nodes belonging to the element
    HMatrix:    H matrix for the element
    '''
    def __init__(self, id: int, IDs: list[int]):
        self.id = id
        self.IDs = IDs
        self.HMatrix = None

    def calculateHMatrix(self, nodes: list[Node], uEl: UniversalElement, glData: GlobalData) -> None:
        '''
        Calculates H matrix for the element.
        '''
        xCoords, yCoords = self.fillXYCoords(nodes)
        dXdKsiTab, dXdEtaTab, dYdKsiTab, dYdEtaTab = self.fillXYKsiEtaTabs(xCoords, yCoords, uEl)
        dNdXTab, dNdYTab, detTab = self.fillDNdXdNdYTabs(dXdKsiTab, dXdEtaTab, dYdKsiTab, dYdEtaTab, uEl)
        ipHMatrices = self.calculateHMatrixForIntegrationPoints(dNdXTab, dNdYTab, detTab, uEl.n, glData.conductivity)
        
        self.HMatrix = np.zeros((4, 4))
        for i in range(0, uEl.n*uEl.n):
            #print(ipHMatrices[i])
            self.HMatrix += ipHMatrices[i]*(uEl.weights[i//uEl.n])*(uEl.weights[i%uEl.n])

    def fillXYCoords(self, nodes: list[Node]) -> tuple[float]:
        '''
        Fills lists storing x and y coords of nodes belonging to the element.
        '''
        xCoords = []; yCoords = []
        for i in range(0, 4):
            xCoords.append(nodes[i].x)
            yCoords.append(nodes[i].y)
        #print(f"xCoords: {xCoords}\nyCoords: {yCoords}")
        return xCoords, yCoords
    
    def fillXYKsiEtaTabs(self, xCoords: list[float], yCoords: list[float], uEl: UniversalElement) -> tuple[list[float]]:
        '''
        Calculates dx/dksi, dx/deta, dy/dksi, dy/deta for every integration point and returns 4 tables with output.
        '''
        dXdKsiTab = []; dXdEtaTab = []; dYdKsiTab = []; dYdEtaTab = []
        for i in range(0, uEl.n*uEl.n):
            dXdKsiTab.append(self.dKsi(uEl.dNdKsiTab[i][0], uEl.dNdKsiTab[i][1], uEl.dNdKsiTab[i][2], uEl.dNdKsiTab[i][3], xCoords))
            dXdEtaTab.append(self.dEta(uEl.dNdEtaTab[i][0], uEl.dNdEtaTab[i][1], uEl.dNdEtaTab[i][2], uEl.dNdEtaTab[i][3], xCoords))
            dYdKsiTab.append(self.dKsi(uEl.dNdKsiTab[i][0], uEl.dNdKsiTab[i][1], uEl.dNdKsiTab[i][2], uEl.dNdKsiTab[i][3], yCoords))
            dYdEtaTab.append(self.dKsi(uEl.dNdEtaTab[i][0], uEl.dNdEtaTab[i][1], uEl.dNdEtaTab[i][2], uEl.dNdEtaTab[i][3], yCoords))
        #print(f"dXdKsiTab: {dXdKsiTab}\ndXdEtaTab: {dXdEtaTab}\ndYdKsiTab: {dYdKsiTab}\ndYdEtaTab: {dYdEtaTab}")
        return dXdKsiTab, dXdEtaTab, dYdKsiTab, dYdEtaTab
    
    def fillDNdXdNdYTabs(self, dXdKsiTab: list, dXdEtaTab: list, dYdKsiTab: list, dYdEtaTab: list, uEl: UniversalElement) -> tuple[list[float]]:
        '''
        Fills dN/dx and dN/dy tables and calculates Jacobian and det[J].

        mxJ: Jacobian matrix
        detJ: Jacobian determinant
        '''
        dNdXTab, dNdYTab = self.initializeDNdXdNdYTabs(uEl.n)
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
    
    def initializeDNdXdNdYTabs(self, n: int) -> tuple[list[list]]:
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

    def calculateHMatrixForIntegrationPoints(self, dNdXTab: list, dNdYTab: list, detTab: list, n: int, k: int) -> list[np.ndarray]:
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

    def dKsi(self, dN1dKsi: float,
                     dN2dKsi: float,
                     dN3dKsi: float,
                     dN4dKsi: float,
                     var: float) -> float:
        '''
        Returns dx/dksi or dy/dksi depending on the argument given.
        '''
        return dN1dKsi*var[0] + dN2dKsi*var[1] + dN3dKsi*var[2] + dN4dKsi*var[3]

    def dEta(self, dN1dEta: float,
                     dN2dEta: float,
                     dN3dEta: float,
                     dN4dEta: float,
                     var: float) -> float:
        '''
        Returns dx/deta or dy/deta depending on the argument given.
        '''
        return dN1dEta*var[0] + dN2dEta*var[1] + dN3dEta*var[2] + dN4dEta*var[3]

    def print(self) -> None:
        print(f"Element {self.id}: \t{self.IDs}")

class Grid:
    '''
    Stores information allowing to recreate the grid.

    globalData:     i.e. simulation time, conductivity, initial temperature, density etc.
    nodes:          list of nodes in the grid
    elements:       list of elements in the grid
    '''
    def __init__(self, inputFile: str = None, globalData: GlobalData = None, elements: list[Element] = None, nodes: list[Node] = None):
        if inputFile is not None:
            f = open(inputFile, "r")
            fileContent = f.readlines()
            self.globalData = self.ReadGlobalData(fileContent)
            self.nodes = self.ReadNodes(fileContent, self.globalData.nodesNumber)
            self.elements = self.ReadElements(fileContent, self.globalData.nodesNumber, self.globalData.elementsNumber)
            f.close()
        elif globalData is not None and elements is not None and nodes is not None:
            self.globalData = globalData
            self.nodes = nodes
            self.elements = elements
        else:
            raise MyException("Not enough input data to create a grid")

    def ReadGlobalData(self, input: str) -> GlobalData:
        '''
        Reads global data from input file.
        '''
        globalDataDict = {}
        for i in range (0, 8):
            line = input[i]
            line = line.split(" ")
            for i in range (0, 2):
                line[i] = line[i].strip()
            globalDataDict[line[0]] = int(line[1])
        for i in range (8, 10):
            line = input[i]
            line = line.split(" ")
            for i in range (0, 3):
                line[i] = line[i].strip()
            line[0] = line[0] + line[1]
            globalDataDict[line[0]] = int(line[2])
        return GlobalData(globalDataDict)

    def ReadNodes(self, input: str, nodesNumber: int) -> list[Node]:
        '''
        Reads nodes from input file.
        '''
        nodeList = []
        for i in range (11, 11 + nodesNumber):
            line = input[i].split(", ")
            nodeList.append(Node(int(line[0]), float(line[1]), float(line[2])))
        return nodeList

    def ReadElements(self, input: str, nodesNumber: int, elementsNumber: int) -> list[Element]:
        '''
        Reads elements data from input file.
        '''
        elements = []
        nodeIDs = []
        for i in range (11 + nodesNumber + 1, 11 + nodesNumber + 1 + elementsNumber):
            line = input[i].split(", ")
            for i in range (1, len(line)):
                nodeIDs.append(int(line[i]))
            elements.append(Element(int(line[0]), nodeIDs))
            nodeIDs = []
        return elements
    
    def calculateHMatrices(self, n: int) -> None:
        '''
        Calculates H matrices for each element in the grid, output is stored in Element.Hmatrix.
        '''
        uEl = UniversalElement(n)
        for element in self.elements:
            element.calculateHMatrix([self.nodes[element.IDs[0] - 1],
                                      self.nodes[element.IDs[1] - 1],
                                      self.nodes[element.IDs[2] - 1],
                                      self.nodes[element.IDs[3] - 1]],
                                      uEl, self.globalData)
            print(element.HMatrix)
    
    def print(self) -> None:
        self.globalData.print()
        print("\nNodes:")
        for node in self.nodes:
            node.print()
        print("\nElements:")
        for element in self.elements:
            element.print()
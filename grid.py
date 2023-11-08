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

    def calculateHMatrix(self, nodes: list[Node], uEl: UniversalElement):
        '''
        Calculates H matrix for the element.
        '''
        xCoords, yCoords = self.fillXYCoords(nodes)
        print(f"xCoords: {xCoords}\nyCoords: {yCoords}")
        dXdKsiTab, dXdEtaTab, dYdKsiTab, dYdEtaTab = self.fillXYKsiEtaTabs(xCoords, yCoords, uEl)
        print(f"dXdKsiTab: {dXdKsiTab}\ndXdEtaTab: {dXdEtaTab}\ndYdKsiTab: {dYdKsiTab}\ndYdEtaTab: {dYdEtaTab}")
        dNdXTab, dNdYTab = self.filldNdXdNdYTabs(dXdKsiTab, dXdEtaTab, dYdKsiTab, dYdEtaTab, uEl)
        print("dNdXTab:")
        print2dTab(dNdXTab)
        print("dNdYTab:")
        print2dTab(dNdYTab)
        self.calculateHMatrixForIntegrationPoints()      

    def fillXYCoords(self, nodes: list[Node]):
        '''
        Fills lists storing x and y coords of nodes belonging to the element.
        '''
        xCoords = []; yCoords = []
        for i in range(0, 4):
            xCoords.append(nodes[i].x)
            yCoords.append(nodes[i].y)
        return xCoords, yCoords
    
    def fillXYKsiEtaTabs(self, xCoords: list[float], yCoords: list[float], uEl: UniversalElement):
        '''
        Calculates dx/dksi, dx/deta, dy/dksi, dy/deta for every integration point and saves the output in tables.
        '''
        dXdKsiTab = []; dXdEtaTab = []; dYdKsiTab = []; dYdEtaTab = []
        for i in range(0, uEl.n*uEl.n):
            dXdKsiTab.append(self.dKsi(uEl.dNdKsiTab[i][0], uEl.dNdKsiTab[i][1], uEl.dNdKsiTab[i][2], uEl.dNdKsiTab[i][3], xCoords))
            dXdEtaTab.append(self.dEta(uEl.dNdEtaTab[i][0], uEl.dNdEtaTab[i][1], uEl.dNdEtaTab[i][2], uEl.dNdEtaTab[i][3], xCoords))
            dYdKsiTab.append(self.dKsi(uEl.dNdKsiTab[i][0], uEl.dNdKsiTab[i][1], uEl.dNdKsiTab[i][2], uEl.dNdKsiTab[i][3], yCoords))
            dYdEtaTab.append(self.dKsi(uEl.dNdEtaTab[i][0], uEl.dNdEtaTab[i][1], uEl.dNdEtaTab[i][2], uEl.dNdEtaTab[i][3], yCoords))
        return dXdKsiTab, dXdEtaTab, dYdKsiTab, dYdEtaTab
    
    def filldNdXdNdYTabs(self, dXdKsiTab: list, dXdEtaTab: list, dYdKsiTab: list, dYdEtaTab: list, uEl: UniversalElement):
        '''
        Fills dN/dx and dN/dy tables.
        '''
        dNdXTab, dNdYTab = self.initializeTabs(uEl.n)
        for j in range(uEl.n*uEl.n):
            mx1 = np.array([[dXdKsiTab[j], dYdKsiTab[j]],
                             [dXdEtaTab[j], dYdEtaTab[j]]])
            mx1Det = np.linalg.det(mx1)
            #print(f"mx1*(1/det): {mx1*(1/mx1Det)}")
            for i in range (0, 4):
                mx2 = np.array([[uEl.dNdKsiTab[j][i]],[uEl.dNdEtaTab[j][i]]])
                #print(f"mx2: {mx2}")
                mxOutput = np.matmul(((1/mx1Det)*mx1), mx2)
                #print(f"mxOutput: {mxOutput}")
                #print(f"mxOutput[0] = {mxOutput[0]}")
                #print(f"mxOutput[1] = {mxOutput[1]}")
                dNdXTab[j][i] = mxOutput[0][0]
                dNdYTab[j][i] = mxOutput[1][0]
                #self.dNdKsiTab[j][i] = self.dNdKsiFunTab[i](self.points[j//self.n])
                #self.dNdEtaTab[j][i] = self.dNdEtaFunTab[i](self.points[j%self.n])
        return dNdXTab, dNdYTab

    def calculateHMatrixForIntegrationPoints():
        pass

    def initializeTabs(self, n: int):
        dNdXTab = []; dNdYTab = []
        for j in range(n*n):
            dNdXTab.append([])
            dNdYTab.append([])
            for i in range (0, 4):
                dNdXTab[j].append(0)
                dNdYTab[j].append(0)
        return dNdXTab, dNdYTab

    def dKsi(self, dN1dKsi: float,
                     dN2dKsi: float,
                     dN3dKsi: float,
                     dN4dKsi: float,
                     var: float) -> float:
        return dN1dKsi*var[0] + dN2dKsi*var[1] + dN3dKsi*var[2] + dN4dKsi*var[3]

    def dEta(self, dN1dEta: float,
                     dN2dEta: float,
                     dN3dEta: float,
                     dN4dEta: float,
                     var: float) -> float:
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
        nodeList = []
        for i in range (11, 11 + nodesNumber):
            line = input[i].split(", ")
            nodeList.append(Node(int(line[0]), float(line[1]), float(line[2])))
        return nodeList

    def ReadElements(self, input: str, nodesNumber: int, elementsNumber: int) -> list[Element]:
        elements = []
        nodeIDs = []
        for i in range (11 + nodesNumber + 1, 11 + nodesNumber + 1 + elementsNumber):
            line = input[i].split(", ")
            for i in range (1, len(line)):
                nodeIDs.append(int(line[i]))
            elements.append(Element(int(line[0]), nodeIDs))
            nodeIDs = []
        return elements
    
    def calculateHMatrices(self, n: int):
        '''
        Calculates H matrices for each element in the grid.
        '''
        uEl = UniversalElement(n)
        for element in self.elements:
            element.calculateHMatrix([self.nodes[element.IDs[0] - 1],
                                      self.nodes[element.IDs[1] - 1],
                                      self.nodes[element.IDs[2] - 1],
                                      self.nodes[element.IDs[3] - 1]],
                                      uEl)

    def calculateHMatrix(self):
        pass

    def calculateJacobian(self):
        pass

    def calculateDet(self):
        pass
    
    def print(self) -> None:
        self.globalData.print()
        print("\nNodes:")
        for node in self.nodes:
            node.print()
        print("\nElements:")
        for element in self.elements:
            element.print()
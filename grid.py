from common import *
from universal_element import *

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
    BC:      border condition (0 or 1)
    '''
    def __init__(self, id: int, x: float, y: float):
        self.id = id
        self.x = x
        self.y = y
        self.BC = 0

    def print(self) -> None:
        print(f"Node {self.id}: \t({self.x}, {self.y})")

class Element:
    '''
    Stores information about a single 4-node element of the grid.

    id:         Element's ID
    IDs:        IDs od nodes belonging to the element
    H:    H matrix for the element
    HBCMatrix
    '''
    def __init__(self, id: int, IDs: list[int]):
        self.id = id
        self.IDs = IDs
        self.H = None
        self.HBCMatrix = None

    def print(self) -> None:
        print(f"Element {self.id}: \t{self.IDs}")

class Grid:
    '''
    Stores information allowing to recreate the grid.

    globalData:     i.e. simulation time, conductivity, initial temperature, density etc.
    nodes:          list of nodes in the grid
    elements:       list of elements in the grid
    BC:             list of nodes with border condition
    '''
    def __init__(self, inputFile: str = None, globalData: GlobalData = None, elements: list[Element] = None, nodes: list[Node] = None):
        if inputFile is not None:
            f = open(inputFile, "r")
            fileContent = f.readlines()
            self.globalData = self.ReadGlobalData(fileContent)
            self.nodes = self.ReadNodes(fileContent, self.globalData.nodesNumber)
            self.elements = self.ReadElements(fileContent, self.globalData.nodesNumber, self.globalData.elementsNumber)
            self.BC = self.ReadBC(fileContent, self.globalData.nodesNumber, self.globalData.elementsNumber)
            self.AddBcToNode(self.BC)
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
    
    def ReadBC(self, input: str, nodesNumber: int, elementsNumber: int) -> list[int]:
        '''
        Reads nodes with border condition from input file.
        '''
        nodeIDs = []
        line = input[11 + nodesNumber + 1 + elementsNumber + 1]
        line = line.split(", ")
        for i in range(0, len(line)):
            nodeIDs.append(int(line[i]))
        return nodeIDs
    
    def AddBcToNode(self, BC: list[int]) -> None:
        '''
        Adds border condition to node.
        '''
        for nodeID in BC:
            self.nodes[nodeID - 1].BC = 1
    
    def print(self) -> None:
        self.globalData.print()
        print("\nNodes:")
        for node in self.nodes:
            node.print()
        print("\nElements:")
        for element in self.elements:
            element.print()
        print(f"\nBC:\n{self.BC}")
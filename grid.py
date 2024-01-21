from common import *
from universal_element import *
import numpy as np

class GlobalData:
    '''
    Stores general information like simulation time, conductivity, initial temperature, density etc.
    '''
    def __init__(self, globalDataDict: dict):
        self.simulationTime: float = globalDataDict['SimulationTime']
        self.simulationStepTime: float = globalDataDict['SimulationStepTime']
        self.conductivity: float = globalDataDict['Conductivity']
        self.alfa: float = globalDataDict['Alfa']
        self.tot: float = globalDataDict['Tot']
        self.initialTemp: float = globalDataDict['InitialTemp']
        self.density: float = globalDataDict['Density']
        self.specificHeat: float = globalDataDict['SpecificHeat']
        self.nodesNumber: int = globalDataDict['Nodesnumber']
        self.elementsNumber: int = globalDataDict['Elementsnumber']

    def print(self) -> None:
        print(f'Simulation time: \t{self.simulationTime}')
        print(f'Simulation step time: \t{self.simulationStepTime}')
        print(f'Conductivity: \t\t{self.conductivity}')
        print(f'Alfa: \t\t\t{self.alfa}')
        print(f'Tot: \t\t\t{self.tot}')
        print(f'Initial temp: \t\t{self.initialTemp}')
        print(f'Density: \t\t{self.density}')
        print(f'Specific heat: \t\t{self.specificHeat}')
        print(f'Nodes number: \t\t{self.nodesNumber}')
        print(f'Elements number: \t{self.elementsNumber}')

class Node:
    '''
    Stores information about a single node of the grid.

    id:      Node's ID
    x:       x coord
    y:       y coord
    BC:      border condition (0 or 1)
    '''
    def __init__(self, id: int, x: float, y: float):
        self.id: int = id
        self.x: float = x
        self.y: float = y
        self.BC: float = 0

    def print(self) -> None:
        print(f'Node {self.id}: \t({self.x}, {self.y})')

class Element:
    '''
    Stores information about a single 4-node element of the grid.

    id:         Element's ID
    IDs:        IDs od nodes belonging to the element
    H:          H matrix for the element (4x4)
    Hbc:        Hbc matrix for the element (4x4)
    P:          P vector for the element (4X1)
    C:          C matrix for the element (4x4)
    '''
    def __init__(self, id: int, nodeIds: list[int]):
        self.id: int = id
        self.nodeIds: list[int] = nodeIds
        self.H: np.ndarray = np.zeros((4, 4))
        self.Hbc: np.ndarray = np.zeros((4, 4))
        self.P: np.ndarray = np.zeros((4, 1))
        self.C: np.ndarray = np.zeros((4, 4))

    def print(self) -> None:
        print(f'Element {self.id}: \t{self.nodeIds}')

class Grid:
    '''
    Stores information allowing to recreate the grid.

    globalData:     i.e. simulation time, conductivity, initial temperature, density etc.
    nodes:          list of nodes in the grid
    elements:       list of elements in the grid
    BC:             list of nodes with border condition
    '''
    def __init__(self, globalData: GlobalData = None, elements: list[Element] = None, nodes: list[Node] = None):
        self.globalData: GlobalData = globalData
        self.nodes: list[Node] = nodes
        self.elements: list[Element] = elements
        
    @classmethod
    def createFromFile(cls, inputFilePath: str):
        try:
            print(os.path.basename(inputFilePath))
            f = open(inputFilePath, 'r')
            fileContent: str = f.readlines()
            globalData: GlobalData = cls._readGlobalData(fileContent)
            nodes: list[Node] = cls._readNodes(fileContent, globalData.nodesNumber)
            elements: list[Element] = cls._readElements(fileContent, globalData.nodesNumber, globalData.elementsNumber)
            BC: list[Node] = cls._readBC(fileContent, globalData.nodesNumber, globalData.elementsNumber)
            cls._addBcToNode(nodes, BC)
            f.close()
            return cls(globalData, elements, nodes)
        except Exception as e:
            raise FiniteElementMethodException(f'Error while creating a Grid object. Check if your input file format is correct. Error:\n{e}')

    @staticmethod
    def _readGlobalData(input: str) -> GlobalData:
        '''
        Reads global data from input file.
        '''
        globalDataDict = {}
        for i in range (0, 8):
            line = input[i]
            line = line.split(' ')
            for i in range (0, 2):
                line[i] = line[i].strip()
            globalDataDict[line[0]] = int(line[1])
        for i in range (8, 10):
            line = input[i]
            line = line.split(' ')
            for i in range (0, 3):
                line[i] = line[i].strip()
            line[0] = line[0] + line[1]
            globalDataDict[line[0]] = int(line[2])
        return GlobalData(globalDataDict)

    @staticmethod
    def _readNodes(input: str, nodesNumber: int) -> list[Node]:
        '''
        Reads nodes from input file.
        '''
        nodeList = []
        for i in range (11, 11 + nodesNumber):
            line = input[i].split(', ')
            nodeList.append(Node(int(line[0]), float(line[1]), float(line[2])))
        return nodeList

    @staticmethod
    def _readElements(input: str, nodesNumber: int, elementsNumber: int) -> list[Element]:
        '''
        Reads elements data from input file.
        '''
        elements = []
        nodeIds = []
        for i in range (11 + nodesNumber + 1, 11 + nodesNumber + 1 + elementsNumber):
            line = input[i].split(', ')
            for i in range (1, len(line)):
                nodeIds.append(int(line[i]))
            elements.append(Element(int(line[0]), nodeIds))
            nodeIds = []
        return elements
    
    @staticmethod
    def _readBC(input: str, nodesNumber: int, elementsNumber: int) -> list[int]:
        '''
        Reads nodes with border condition from input file.
        '''
        nodeIDs = []
        line = input[11 + nodesNumber + 1 + elementsNumber + 1]
        line = line.split(', ')
        for i in range(0, len(line)):
            nodeIDs.append(int(line[i]))
        return nodeIDs
    
    @staticmethod
    def _addBcToNode(nodes: list[Node], BC: list[int]) -> None:
        '''
        Adds border condition to node.
        '''
        for nodeID in BC:
            nodes[nodeID - 1].BC = 1
    
    def print(self) -> None:
        self.globalData.print()
        print('\nNodes:')
        for node in self.nodes:
            node.print()
        print('\nElements:')
        for element in self.elements:
            element.print()
        print(f'\nBC:\n{self.BC}\n')
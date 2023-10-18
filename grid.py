class GlobalData:
    def __init__(self, globalData: dict):
        self.simulationTime = globalData["SimulationTime"]
        self.simulationStepTime = globalData["SimulationStepTime"]
        self.conductivity = globalData["Conductivity"]
        self.alfa = globalData["Alfa"]
        self.tot = globalData["Tot"]
        self.initialTemp = globalData["InitialTemp"]
        self.density = globalData["Density"]
        self.specificHeat = globalData["SpecificHeat"]
        self.nodesNumber = globalData["Nodesnumber"]
        self.elementsNumber = globalData["Elementsnumber"]

class Node:
    def __init__(self, id: int, x: float, y: float):
        self.id = id
        self.x = x
        self.y = y
    def print_node(self):
        print(self.x, self.y)

class Element:
    def __init__(self, id: int, ID: list[int]):
        self.id = id
        self.ID = ID

class Grid:
    def __init__(self, elements: list, nodes: list):
        self.elements = elements
        self.nodes = nodes

def ReadGrid(inputFile: str) -> Grid:
    f = open(inputFile, "r")
    fileContent = f.readlines()
    globalDataObj = ReadGlobalData(fileContent)
    nodeList = ReadNodes(fileContent, globalDataObj.nodesNumber)
    elementList = ReadElements(fileContent, globalDataObj.nodesNumber, globalDataObj.elementsNumber)
    f.close()
    return Grid(elementList, nodeList)

def ReadGlobalData(input: str) -> GlobalData:
    globalData = {}
    for i in range (0, 8):
        line = input[i]
        line = line.split(" ")
        for i in range (0, 2):
            line[i] = line[i].strip()
        globalData[line[0]] = int(line[1])
    for i in range (8, 10):
        line = input[i]
        line = line.split(" ")
        for i in range (0, 3):
            line[i] = line[i].strip()
        line[0] = line[0] + line[1]
        globalData[line[0]] = int(line[2])
    return GlobalData(globalData)

def ReadNodes(input: str, nodesNumber: int) -> list[Node]:
    nodeList = []
    for i in range (11, 11 + nodesNumber):
        line = input[i].split(", ")
        nodeList.append(Node(int(line[0]), float(line[1]), float(line[2])))
    return nodeList

def ReadElements(input: str, nodesNumber: int, elementsNumber: int) -> list[Element]:
    elementList = []
    tempList = []
    for i in range (11 + nodesNumber + 1, 11 + nodesNumber + 1 + elementsNumber):
        line = input[i].split(", ")
        for i in range (1, len(line)):
            tempList.append(int(line[i]))
        elementList.append(Element(int(line[0]), tempList))
        tempList = []
    return elementList
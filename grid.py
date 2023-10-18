class GlobalData:
    def __init__(self, globalDataDict: dict) -> None:
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

    def printGlobalData(self):
        print(f"Simulation time: \t{self.simulationTime}")
        print(f"Simulation step time: \t{self.simulationStepTime}")
        print(f"Conductivity: \t{self.conductivity}")
        print(f"Alfa: \t{self.alfa}")
        print(f"Tot: \t{self.tot}")
        print(f"Initial temp: \t{self.initialTemp}")
        print(f"Density: \t{self.density}")
        print(f"Specific heat: \t{self.specificHeat}")
        print(f"Nodes number: \t{self.nodesNumber}")
        print(f"Elements number: \t{self.elementsNumber}")

class Node:
    def __init__(self, id: int, x: float, y: float) -> None:
        self.id = id
        self.x = x
        self.y = y

    def printNode(self) -> None:
        print(f"Node {self.id}: \t({self.x}, {self.y})")

class Element:
    def __init__(self, id: int, IDs: list[int]) -> None:
        self.id = id
        self.IDs = IDs

    def printElement(self) -> None:
        print(f"Element {self.id}: \t{self.IDs}")

class Grid:
    def __init__(self, inputFile: str) -> None:
        f = open(inputFile, "r")
        fileContent = f.readlines()
        self.globalDataObj = self.ReadGlobalData(fileContent)
        self.nodes = self.ReadNodes(fileContent, self.globalDataObj.nodesNumber)
        self.elements = self.ReadElements(fileContent, self.globalDataObj.nodesNumber, self.globalDataObj.elementsNumber)
        f.close()

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
        elementList = []
        tempList = []
        for i in range (11 + nodesNumber + 1, 11 + nodesNumber + 1 + elementsNumber):
            line = input[i].split(", ")
            for i in range (1, len(line)):
                tempList.append(int(line[i]))
            elementList.append(Element(int(line[0]), tempList))
            tempList = []
        return elementList
    
    def printGrid(self):
        print(self.globalDataObj.printGlobalData())
        print("\nNodes:")
        for node in self.nodes:
            node.printNode()
        print("\nElements:")
        for element in self.elements:
            element.printElement()
from common import *
from grid import Grid, GlobalData, Element, Node
from temperature_simulation import TemperatureSimulation

# Creates 1-element grid for testing purposes
def createTestGrid() -> Grid:
    globalDataDict = {}
    globalDataDict['SimulationTime'] = 0
    globalDataDict['SimulationStepTime'] = 0
    globalDataDict['Conductivity'] = 30
    globalDataDict['Alfa'] = 25
    globalDataDict['Tot'] = 1200
    globalDataDict['InitialTemp'] = 0
    globalDataDict['Density'] = 7800
    globalDataDict['SpecificHeat'] = 700
    globalDataDict['Nodesnumber'] = 4
    globalDataDict['Elementsnumber'] = 1
    globalData = GlobalData(globalDataDict)
    nodes = [Node(1, 0, 0), Node(2, 0.025, 0), Node(3, 0.025, 0.025), Node(4, 0, 0.025)]
    for node in nodes:
        node.BC = 1
    elements = [Element(1, [1, 2, 3, 4])]
    testGrid = Grid(globalData=globalData, nodes=nodes, elements=elements)
    return testGrid

def main():
    try:
        gridFilepath1 = os.path.join(gridsPath, 'Test1_4_4.txt')
        gridFilepath2 = os.path.join(gridsPath, 'Test2_4_4_MixGrid.txt')
        gridFilepath3 = os.path.join(gridsPath, 'Test3_31_31_kwadrat.txt')
        #TemperatureSimulation.run(gridFilepath1)
        TemperatureSimulation.run(gridFilepath2)
        #TemperatureSimulation.run(gridFilepath3)
    except FiniteElementMethodException as e:
        print(e)

if __name__ == '__main__':
    main()
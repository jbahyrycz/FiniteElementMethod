import os
from grid import *
from numerical_integration import *
from universal_element import *
from H_matrix_calculation import *
from Hbc_matrix_and_P_vector_calculation import *

scriptPath = os.getcwd()
gridsPath = os.path.join(scriptPath, "Data", "Grids")

# Functions for lab 2
def fun1(x: float) -> float:
    return 5*pow(x, 2) + 3*x + 6

def fun2(x: float, y: float) -> float:
    return 5*pow(x, 2)*pow(y, 2) + 3*x*y + 6

# Creates 1-element grid for testing purposes
def createTestGrid() -> Grid:
    globalDataDict = {}
    globalDataDict["SimulationTime"] = 0
    globalDataDict["SimulationStepTime"] = 0
    globalDataDict["Conductivity"] = 30
    globalDataDict["Alfa"] = 25
    globalDataDict["Tot"] = 1200
    globalDataDict["InitialTemp"] = 0
    globalDataDict["Density"] = 0
    globalDataDict["SpecificHeat"] = 0
    globalDataDict["Nodesnumber"] = 4
    globalDataDict["Elementsnumber"] = 1
    globalData = GlobalData(globalDataDict)
    nodes = [Node(1, 0, 0), Node(2, 0.025, 0), Node(3, 0.025, 0.025), Node(4, 0, 0.025)]
    for node in nodes:
        node.BC = 1
    elements = [Element(1, [1, 2, 3, 4])]
    testGrid = Grid(globalData=globalData, nodes=nodes, elements=elements)
    return testGrid

def main():
    try:
        gridObj1, gridObj2, gridObj3 = lab1()
        testGrid = createTestGrid()
        #lab2()
        #lab3()
        #lab4(testGrid, gridObj1, gridObj2, gridObj3)
        #lab5(testGrid, gridObj1, gridObj2, gridObj3)
        lab6(testGrid, gridObj1, gridObj2, gridObj3)
    except MyException as e:
        print(e)

def lab1() -> list[Grid]:
    gridObj1 = Grid(os.path.join(gridsPath, "Test1_4_4.txt"))
    gridObj2 = Grid(os.path.join(gridsPath, "Test2_4_4_MixGrid.txt"))
    gridObj3 = Grid(os.path.join(gridsPath, "Test3_31_31_kwadrat.txt"))
    return gridObj1, gridObj2, gridObj3

def lab2():
    f1n2 = GaussianQuadrature(2, fun1)
    print(f1n2.calculateIntegral1d())
    f1n3 = GaussianQuadrature(3, fun1)
    print(f1n3.calculateIntegral1d())
    f1n4 = GaussianQuadrature(4, fun1)
    print(f1n4.calculateIntegral1d())

    f2n2 = GaussianQuadrature(2, fun2)
    print(f2n2.calculateIntegral2d())
    f2n3 = GaussianQuadrature(3, fun2)
    print(f2n3.calculateIntegral2d())
    f2n4 = GaussianQuadrature(4, fun2)
    print(f2n4.calculateIntegral2d())

def lab3():
    #el2n = UniversalElement(2)
    #print("dN/dKsi:")
    #print2dTab(el2n.dNdKsiTab)
    #print("dN/dEta:")
    #print2dTab(el2n.dNdEta)
    element2 = UniversalElement(3)
    print("dN/dKsi:")
    print2dTab(element2.dNdKsiTab)
    print("dN/dEta:")
    print2dTab(element2.dNdEtaTab)
    #element3 = UniversalElement(4)
    #print("dN/dKsi:")
    #print2dTab(element3.dNdKsiTab)
    #print("dN/dEta:")
    #print2dTab(element3.dNdEta)

def lab4(testGrid: Grid, test1: Grid, test2: Grid, test3: Grid) -> None:
    HMatrixCalculation.calculate(2, testGrid)
    #HMatrixCalculation.calculate(2, test1)
    #HMatrixCalculation.calculate(2, test2)
    #HMatrixCalculation.calculate(2, test3)

def lab5(testGrid: Grid, test1: Grid, test2: Grid, test3: Grid) -> None:
    #HbcMatrixAndPVectorCalculation.calculate(2, testGrid)
    HbcMatrixAndPVectorCalculation.calculate(4, test1)
    #HbcMatrixAndPVectorCalculation.calculate(2, test2)
    #HbcMatrixAndPVectorCalculation.calculate(2, test3)

def lab6(testGrid: Grid, test1: Grid, test2: Grid, test3: Grid) -> None:
    #HbcMatrixAndPVectorCalculation.calculate(2, testGrid)
    HbcMatrixAndPVectorCalculation.calculate(2, test1)
    #HbcMatrixAndPVectorCalculation.calculate(2, test2)
    #HbcMatrixAndPVectorCalculation.calculate(2, test3)
    pass

if __name__ == "__main__":
    main()
import os
from grid import *
from numerical_integration import *
from universal_element import *

scriptPath = os.getcwd()
gridsPath = os.path.join(scriptPath, "Data", "Grids")

# Functions for lab 2
def fun1(x: float) -> float:
    return 5*pow(x, 2) + 3*x + 6

def fun2(x: float, y: float) -> float:
    return 5*pow(x, 2)*pow(y, 2) + 3*x*y + 6

def main():
    try:
        #lab1()
        #lab2()
        #lab3()
        lab4()
    except MyException as e:
        print(e)

def lab1():
    gridObj1 = Grid(os.path.join(gridsPath, "Test1_4_4.txt"))
    gridObj1.print()
    gridObj2 = Grid(os.path.join(gridsPath, "Test2_4_4_MixGrid.txt"))
    gridObj3 = Grid(os.path.join(gridsPath, "Test3_31_31_kwadrat.txt"))

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

def lab4():
    '''
    # Test grid
    globalDataDict = {}
    globalDataDict["SimulationTime"] = 0
    globalDataDict["SimulationStepTime"] = 0
    globalDataDict["Conductivity"] = 0
    globalDataDict["Alfa"] = 0
    globalDataDict["Tot"] = 0
    globalDataDict["InitialTemp"] = 0
    globalDataDict["Density"] = 0
    globalDataDict["SpecificHeat"] = 0
    globalDataDict["Nodesnumber"] = 4
    globalDataDict["Elementsnumber"] = 1
    globalData = GlobalData(globalDataDict)
    nodes = [Node(1, 0, 0), Node(2, 0.025, 0), Node(3, 0.025, 0.025), Node(4, 0, 0.025)]
    elements = [Element(1, [1, 2, 3, 4])]
    grid = Grid(globalData=globalData, nodes=nodes, elements=elements)
    #grid.print()

    # Calculations for test grid and n = 2
    n = 4
    grid.calculateHMatrices(n)
    print(grid.elements[0].HMatrix)
    '''
    gridObj1 = Grid(os.path.join(gridsPath, "Test1_4_4.txt"))
    #gridObj1.print()
    #gridObj1.calculateHMatrices(3)
    gridObj2 = Grid(os.path.join(gridsPath, "Test2_4_4_MixGrid.txt"))
    gridObj2.calculateHMatrices(3)
    gridObj3 = Grid(os.path.join(gridsPath, "Test3_31_31_kwadrat.txt"))
    #gridObj3.calculateHMatrices(3)






if __name__ == "__main__":
    main()
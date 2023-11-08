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
        lab3()
    except MyException as e:
        print(e)

def lab1():
    gridObj1 = Grid(os.path.join(gridsPath, "Test1_4_4.txt"))
    gridObj1.print()
    gridObj2 = Grid(os.path.join(gridsPath, "Test2_4_4_MixGrid.txt"))
    gridObj3 = Grid(os.path.join(gridsPath, "Test3_31_31_kwadrat.txt"))

def lab2():
    f1n2 = GaussMethod(2, fun1)
    print(f1n2.calculateIntegral1d())
    f1n3 = GaussMethod(3, fun1)
    print(f1n3.calculateIntegral1d())
    f1n4 = GaussMethod(4, fun1)
    print(f1n4.calculateIntegral1d())

    f2n2 = GaussMethod(2, fun2)
    print(f2n2.calculateIntegral2d())
    f2n3 = GaussMethod(3, fun2)
    print(f2n3.calculateIntegral2d())
    f2n4 = GaussMethod(4, fun2)
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

if __name__ == "__main__":
    main()
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
    f1n2 = GaussMethod(fun1, 2)
    print(f1n2.calculate1d())
    f1n3 = GaussMethod(fun1, 3)
    print(f1n3.calculate1d())
    f1n4 = GaussMethod(fun1, 4)
    print(f1n4.calculate1d())

    f2n2 = GaussMethod(fun2, 2)
    print(f2n2.calculate2d())
    f2n3 = GaussMethod(fun2, 3)
    print(f2n3.calculate2d())
    f2n4 = GaussMethod(fun2, 4)
    print(f2n4.calculate2d())

def lab3():
    #element = UniversalElement()
    #print2dTab(element.dNKsi)
    #print2dTab(element.dNEta)
    element2 = UniversalElement(3)
    print("Ksi:")
    print2dTab(element2.dNKsi)
    print("Eta:")
    print2dTab(element2.dNEta)

if __name__ == "__main__":
    main()
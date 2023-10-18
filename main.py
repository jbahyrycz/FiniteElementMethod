import os
from grid import *
from numerical_integration import *

scriptPath = os.getcwd()
gridsPath = os.path.join(scriptPath, "Data", "Grids")

def fun1(x: float) -> float:
    return 5* x * x + 3 * x + 6

def fun2(x: float, y: float) -> float:
    return 5 * x * x * y * y + 3 * x * y + 6

def main():
    #lab1()
    lab2()

def lab1():
    gridObj1 = Grid(os.path.join(gridsPath, "Test1_4_4.txt"))
    gridObj1.print()
    gridObj2 = Grid(os.path.join(gridsPath, "Test2_4_4_MixGrid.txt"))
    gridObj3 = Grid(os.path.join(gridsPath, "Test3_31_31_kwadrat.txt"))

def lab2():
    f1n2 = NumericalIntegration(fun1, 2)
    print(f1n2.calculate1d())
    f1n3 = NumericalIntegration(fun1, 3)
    print(f1n3.calculate1d())
    f1n4 = NumericalIntegration(fun1, 4)
    print(f1n4.calculate1d())

    f2n2 = NumericalIntegration(fun2, 2)
    print(f2n2.calculate2d())
    f2n3 = NumericalIntegration(fun2, 3)
    print(f2n3.calculate2d())
    f2n4 = NumericalIntegration(fun2, 4)
    print(f2n4.calculate2d())
    
if __name__ == "__main__":
    main()
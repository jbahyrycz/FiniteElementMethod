import os
from grid import *

scriptPath = os.getcwd()
gridsPath = os.path.join(scriptPath, "Data", "Grids")

def main():
    try:
        gridObj1 = Grid(os.path.join(gridsPath, "Test1_4_4.txt"))
        gridObj1.print()
        gridObj2 = Grid(os.path.join(gridsPath, "Test2_4_4_MixGrid.txt"))
        gridObj3 = Grid(os.path.join(gridsPath, "Test3_31_31_kwadrat.txt"))
    except Exception as e:
        print(f"Catched error: {e}")

if __name__ == "__main__":
    main()
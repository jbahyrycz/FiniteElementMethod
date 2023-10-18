import os
from grid import *

scriptPath = os.getcwd()
gridsPath = os.path.join(scriptPath, "Data", "Grids")

def main():
    try:
        gridObj1 = ReadGrid(os.path.join(gridsPath, "Test1_4_4.txt"))
        gridObj1.nodes[0].print_node() # Print first node
        gridObj1.nodes[gridObj1.elements[0].ID[0] - 1].print_node() # Print first node of first element (first node)
        gridObj2 = ReadGrid(os.path.join(gridsPath, "Test2_4_4_MixGrid.txt"))
        gridObj3 = ReadGrid(os.path.join(gridsPath, "Test3_31_31_kwadrat.txt"))
    except Exception as e:
        print(f"Catched error: {e}")

if __name__ == "__main__":
    main()
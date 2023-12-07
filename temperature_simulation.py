import os
from grid import *
from numerical_integration import *
from universal_element import *
from local_matrices_calculation import *
from system_of_equations import *

class TemperatureSimulation():
    def __init__(self):
        raise MyException("TemperatureSimulation is an abstract class, you cannot create an instance of this class.")

    @staticmethod
    def run(inputFile: str):
        '''
        Runs all the necessary functions to calculate max and min temperature of the element in time.
        '''
        print(os.path.basename(inputFile))
        grid = Grid(inputFile)
        LocalMatricesCalculation.calculate(2, grid)
        soe = SystemOfEquations(grid)
        tau0 = 0
        tauK = grid.globalData.simulationTime
        step = grid.globalData.simulationStepTime
        print(f"Time        Min temp    Max temp")
        while tau0 < tauK:
            result = soe.solve()
            print(f"{(soe.dTau):<12}{round(min(result)[0], 3):<12}{round(max(result)[0], 3):<12}")
            tau0+=step
        print("")
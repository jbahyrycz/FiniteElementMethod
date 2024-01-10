from common import *
from grid import Grid
from local_matrices_calculation import LocalMatricesCalculation
from system_of_equations import SystemOfEquations

class TemperatureSimulation:
    def __init__(self):
        raise FiniteElementMethodException('TemperatureSimulation is an abstract class, you cannot create an instance of this class.')
    
    @staticmethod
    def generateVtkFiles(inputFile: str, grid: Grid, temperatures: list) -> None:
        '''
        Creates files for simulation in ParaView environment.
        '''
        numOfFiles = len(temperatures)
        elementNodesNumber = []
        for element in grid.elements:
            elementNodesNumber.append(len(element.IDs))

        data = {}
        data['nodesNumber'] = grid.globalData.nodesNumber
        data['nodes'] = grid.nodes
        data['elementsNumber'] = grid.globalData.elementsNumber
        data['elements'] = grid.elements
        data['elementNodesNumber'] = elementNodesNumber
        data['sumOfElementsData'] = grid.globalData.elementsNumber + sum(elementNodesNumber)
        destinationDir = os.path.join(outputPath, os.path.basename(inputFile).split('.')[0])

        createOrClearDirectory(destinationDir)
        template = initializeJinjaEnvironment('temperatures.vtk')
        for i in range(0, numOfFiles):
            data['temperatures'] = temperatures[i]
            filename = f'frame{i+1}.vtk'
            generateFile(data, template, destinationDir, filename)
        print(f'Output files generated in {destinationDir}')

    @staticmethod
    def run(inputFile: str) -> None:
        '''
        Runs all the necessary functions to calculate max and min temperature of the element in time.
        '''
        temperatures = []
        print(os.path.basename(inputFile))
        grid = Grid(inputFile)
        LocalMatricesCalculation.calculate(2, grid)
        soe = SystemOfEquations(grid)
        tau0 = 0
        tauK = grid.globalData.simulationTime
        step = grid.globalData.simulationStepTime
        print(f'Time        Min temp    Max temp')
        while tau0 < tauK:
            result = soe.solve()
            temperatures.append(result)
            print(f'{(soe.dTau):<12}{round(min(result)[0], 3):<12}{round(max(result)[0], 3):<12}')
            tau0+=step
        print('')
        TemperatureSimulation.generateVtkFiles(inputFile, grid, temperatures)
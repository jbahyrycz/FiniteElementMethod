import os, shutil
from grid import *
from numerical_integration import *
from universal_element import *
from local_matrices_calculation import *
from system_of_equations import *
from jinja2 import *

class TemperatureSimulation():
    def __init__(self):
        raise MyException("TemperatureSimulation is an abstract class, you cannot create an instance of this class.")
    
    @staticmethod
    def generateVtkFiles(inputFile: str, grid: Grid, temperatures: list):
        '''
        Creates files for simulation in ParaView environment.
        '''
        templatesPath = os.path.join(scriptPath, 'Data', 'Templates')
        environment = Environment(loader=FileSystemLoader(templatesPath))
        template = environment.get_template('temperatures.txt')

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
        outputDirectory = os.path.join(scriptPath, 'Data', 'Output', os.path.basename(inputFile).split('.')[0])

        try:
            os.mkdir(outputDirectory)
        except FileExistsError:
            for filename in os.listdir(outputDirectory):
                try:
                    filepath = os.path.join(outputDirectory, filename)
                    if os.path.isfile(filepath) or os.islink(filepath):
                        os.unlink(filepath)
                    elif os.path.isdir(filepath):
                        shutil.rmtree(filepath)
                except Exception as e:
                    print(f'Failed to delete {filepath}, error:\n{e}')

        for i in range(0, numOfFiles):
            data['temperatures'] = temperatures[i]
            filename = f'frame{i+1}.vtk'
            #directory = inputFile.split('.')[0]
            #filepath = os.path.join(directory, filename)
            outputFilepath = os.path.join(outputDirectory, filename)
            content = template.render(data)
            with open(outputFilepath, mode='w', encoding='utf-8') as file:
                file.write(content)
        print(f'Output files generated in {outputDirectory}')

    @staticmethod
    def run(inputFile: str):
        '''
        Runs all the necessary functions to calculate max and min temperature of the element in time.
        '''
        temperatures = []
        print(os.path.basename(inputFile))
        grid = Grid(inputFile)
        LocalMatricesCalculation.calculate(3, grid)
        soe = SystemOfEquations(grid)
        tau0 = 0
        tauK = grid.globalData.simulationTime
        step = grid.globalData.simulationStepTime
        print(f"Time        Min temp    Max temp")
        while tau0 < tauK:
            result = soe.solve()
            temperatures.append(result)
            print(f"{(soe.dTau):<12}{round(min(result)[0], 3):<12}{round(max(result)[0], 3):<12}")
            tau0+=step
        print("")
        TemperatureSimulation.generateVtkFiles(inputFile, grid, temperatures)
from common import *
from grid import Grid, Element, Node
from jinja2 import Template
from local_matrices_calculation import LocalMatricesCalculation
from system_of_equations import SystemOfEquations
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np

def getInputFilePath() -> str:
    '''
    Gets path to grid file from user.
    '''
    Tk().withdraw()
    inputFilePath: str = askopenfilename()
    return inputFilePath

def simulate(grid: Grid) -> list[np.ndarray]:
    '''
    Returns temeratures in element nodes for all time steps.
    '''
    temperatures: list[np.ndarray] = []
    soe = SystemOfEquations(grid)
    tau0: int = 0
    tauK: float = grid.globalData.simulationTime
    step: float = grid.globalData.simulationStepTime
    print(f'Time        Min temp    Max temp')
    while tau0 < tauK:
        result: np.ndarray = soe.solve()
        temperatures.append(result)
        print(f'{(soe.dTau):<12}{round(min(result)[0], 3):<12}{round(max(result)[0], 3):<12}')
        tau0+=step
    print('')
    return temperatures

def generateVtkFiles(inputFilename: str, grid: Grid, temperatures: list[np.ndarray]) -> None:
    '''
    Creates files for simulation in ParaView environment.
    '''
    numOfFiles: int = len(temperatures)
    elementNodesNumber: int = []
    for element in grid.elements:
        elementNodesNumber.append(len(element.nodeIds))

    data: dict = {}
    data['nodesNumber']: int = grid.globalData.nodesNumber
    data['nodes']: list[Node] = grid.nodes
    data['elementsNumber']: int = grid.globalData.elementsNumber
    data['elements']: list[Element] = grid.elements
    data['elementNodesNumber']: int = elementNodesNumber
    data['sumOfElementsData']: int = grid.globalData.elementsNumber + sum(elementNodesNumber)
    
    destinationDir: str = createOrClearDirectory(inputFilename)
    template: Template = initializeJinjaEnvironment('temperatures.vtk.jinja')
    for i in range(0, numOfFiles):
        data['temperatures']: np.ndarray = temperatures[i]
        filename: str = f'frame{i+1}.vtk'
        generateFile(data, template, destinationDir, filename)
    print(f'Output files generated in {destinationDir}')

def run() -> None:
    '''
    Runs all the necessary functions to calculate max and min temperature of the element in time.
    '''
    try:
        inputFilePath: str = getInputFilePath()
        grid = Grid.createFromFile(inputFilePath)
        LocalMatricesCalculation.calculate(5, grid)
        temperatures: list[float] = simulate(grid)
        generateVtkFiles(inputFilePath, grid, temperatures)
    except FiniteElementMethodException as e:
        print(e)

if __name__ == '__main__':
    run()
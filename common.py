import os
from jinja2 import Environment, FileSystemLoader, Template

scriptPath: str = os.getcwd()
gridsPath: str = os.path.join(scriptPath, 'Data', 'Grids')
outputPath: str = os.path.join(scriptPath, 'Data', 'Output')
templatesPath: str = os.path.join(scriptPath, 'Data', 'Templates')

class FiniteElementMethodException(Exception):
    pass

def createOrClearDirectory(inputFilename: str) -> str:
    try:
        os.mkdir(outputPath)
    except FileExistsError:
        pass
    dirPath = os.path.join(outputPath, os.path.basename(inputFilename).split('.')[0])

    try:
        os.mkdir(dirPath)
    except FileExistsError:
        for filename in os.listdir(dirPath):
            try:
                filepath = os.path.join(dirPath, filename)
                if os.path.isfile(filepath) or os.islink(filepath):
                    os.unlink(filepath)
                elif os.path.isdir(filepath):
                    dirPath.rmtree(filepath)
            except Exception as e:
                raise FiniteElementMethodException(f'Error while claring output directory {dirPath}.\nFailed to delete {os.path.basename(filepath)}. Error:\n{e}')
    finally:
        return dirPath
    
def initializeJinjaEnvironment(templateFile: str) -> Template:
    environment = Environment(loader=FileSystemLoader(templatesPath))
    template = environment.get_template(templateFile)
    return template

def generateFile(data: dict, template: Template, destinationDir: str, outputFileName: str) -> None:
    outputFilepath = os.path.join(destinationDir, outputFileName)
    content = template.render(data)
    with open(outputFilepath, mode='w', encoding='utf-8') as file:
        file.write(content)

def print2dTab(tab: list[list]) -> None:
    for innerTab in tab:
        print(innerTab)
    print('\n')
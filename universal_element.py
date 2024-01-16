from common import *
from numerical_integration import GaussianQuadrature
from math import *

class UniversalElement(GaussianQuadrature):
    '''
    Contains all the calculations that are universal for every 4-node element.
    
    dNdKsiTab:      table of dN/dKsi results for N1, N2, N3, N4 in integration points (n^2x4)
    dNdEtaTab:      table of dN/dEta results for N1, N2, N3, N4 in integration points (n^2x4)
    NTab:           table of N(ksi, eta) values for N1, N2, N3, N4 in integration points (nx4)
    surfaces:       list of Surface type elements, necessary for calculations that take border conditions into account
    '''
    def __init__(self, n):
        super().__init__(n, None)
        self.dNdKsiTab: list[list[float]] = []
        self.dNdEtaTab: list[list[float]] = []
        self.NTab: list[list[float]] = []
        self.surfaces: list[Surface] = [
            Surface(n), # down
            Surface(n), # right
            Surface(n), # up
            Surface(n)  # left
        ]
        self.fillTabs()

    def fillTabs(self):
        def initialize():       
            '''
            Initializes empty tables.
            '''
            for i in range(self.n*self.n):
                self.dNdKsiTab.append([])
                self.dNdEtaTab.append([])
                self.NTab.append([])
                for _ in range (0, 4):
                    self.dNdKsiTab[i].append(0)
                    self.dNdEtaTab[i].append(0)
                    self.NTab[i].append(0)

        def filldNdKsidNdEtaTabs():  
            '''
            Calculates dN/dKsi and dN/dEta for N1, N2, N3, N4 in integration points. Result is stored in tables.
            '''
            for j in range(self.n*self.n):
                ksi = self.points[j%self.n]
                eta = self.points[j//self.n]
                for i in range (0, 4):
                    self.dNdKsiTab[j][i] = dNdKsiFunTab[i](eta)
                    self.dNdEtaTab[j][i] = dNdEtaFunTab[i](ksi)
                    self.NTab[j][i] = NFunTab[i](ksi, eta)

        def fillSurfaceTab():
            '''
            Calculates integration points coords for surface calculations.
            '''
            for i in range(0, len(self.surfaces)):
                ksiList = []
                etaList = []
                if i % 2 == 0:
                    ksiList = self.points
                    for _ in range(0, self.n):
                        etaList.append(i - 1)
                else:
                    etaList = self.points
                    for _ in range(0, self.n):
                        ksiList.append(2 - i)
                self.surfaces[i].fillN(ksiList, etaList)

        initialize()
        filldNdKsidNdEtaTabs()
        fillSurfaceTab()

class Surface():
    '''
    Describes the surface of the universal element.
    n:      number of integration points
    N:      table of N(ksi, eta) for N1, N2, N3, N4 and for each integration point on the surface
    '''
    def __init__(self, n: int):
        self.n = n
        self.N = []

    def fillN(self, ksiList: list[float], etaList: list[float]):
        '''
        Calculates N(ksi, eta) for N1, N2, N3, N4 and for each integration point on the surface
        Results are stored in the table
        '''
        def initializeN():
            for i in range (0, self.n):
                self.N.append([])
                for _ in range (0, 4):
                    self.N[i].append(0)
                    
        initializeN()
        for j in range(0, len(ksiList)):
            for i in range(0, 4):
                self.N[j][i] = NFunTab[i](ksiList[j], etaList[j])

def N1(ksi: float, eta: float) -> float:
    return (1/4)*(1-ksi)*(1-eta)

def N2(ksi: float, eta: float) -> float:
    return (1/4)*(1+ksi)*(1-eta)

def N3(ksi: float, eta: float) -> float:
    return (1/4)*(1+ksi)*(1+eta)

def N4(ksi: float, eta: float) -> float:
    return (1/4)*(1-ksi)*(1+eta)

def dN1Ksi(eta: float) -> float:
    return -(1/4)*(1-eta)

def dN2Ksi(eta: float) -> float:
    return (1/4)*(1-eta)

def dN3Ksi(eta: float) -> float:
    return (1/4)*(1+eta)

def dN4Ksi(eta: float) -> float:
    return -(1/4)*(1+eta)

def dN1Eta(ksi: float) -> float:
    return -(1/4)*(1-ksi)

def dN2Eta(ksi: float) -> float:
    return -(1/4)*(1+ksi)

def dN3Eta(ksi: float) -> float:
    return (1/4)*(1+ksi)

def dN4Eta(ksi: float) -> float:
    return (1/4)*(1-ksi)

dNdKsiFunTab = [
    dN1Ksi,
    dN2Ksi,
    dN3Ksi,
    dN4Ksi
]

dNdEtaFunTab = [
    dN1Eta,
    dN2Eta,
    dN3Eta,
    dN4Eta
]
    
NFunTab = [
    N1,
    N2,
    N3,
    N4,
]
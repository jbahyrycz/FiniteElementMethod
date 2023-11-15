from numerical_integration import *
from math import *
from common import *


class UniversalElement(GaussianQuadrature):
    def __init__(self, n):
        super().__init__(n, None)
        self.dNdKsiTab = []
        self.dNdEtaTab = []
        surface = Surface(n)
        self.fillTabs()
            
    def initializeTabs(self):
        for j in range(self.n*self.n):
            self.dNdKsiTab.append([])
            self.dNdEtaTab.append([])
            for i in range (0, 4):
                self.dNdKsiTab[j].append(0)
                self.dNdEtaTab[j].append(0)

    def fillTabs(self):
        '''
        Calculates dN/dKsi and dN/dEta for N1, N2, N3, N4 and in integration points. Result is stored in tables.
        '''
        self.initializeTabs()
        for j in range(self.n*self.n):
            ksi = self.points[j%self.n]
            eta = self.points[j//self.n]
            for i in range (0, 4):
                self.dNdKsiTab[j][i] = dNdKsiFunTab[i](eta)
                self.dNdEtaTab[j][i] = dNdEtaFunTab[i](ksi)

class Surface():
    def __init__(self, n: int):
        self.n = n
        self.N = []
        self.fillN()

    def fillN(self):
        self.initializeN()
        print2dTab(self.N)
        '''
        for j in range(self.n):
            ksi = self.points[j%self.n]
            eta = self.points[j//self.n]
            for i in range (0, 4):
                self.N[j][i] = NFunTab[i](ksi, eta)
        '''
    
    def initializeN(self):
        for j in range (0, self.n):
            self.N.append([])
            for i in range (0, 4):
                self.N[j].append(0)

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
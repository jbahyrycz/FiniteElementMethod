from numerical_integration import GaussMethod
from math import *
from common import *

class UniversalElement(GaussMethod):
    def __init__(self, n):
        super().__init__(n, None)
        self.dNdKsiTab = []
        self.dNdEtaTab = []
        self.dNdKsiFunTab = [
            self.dN1Ksi,
            self.dN2Ksi,
            self.dN3Ksi,
            self.dN4Ksi
        ]
        self.dNdEtaFunTab = [
            self.dN1Eta,
            self.dN2Eta,
            self.dN3Eta,
            self.dN4Eta
        ]
        self.initializeTabs()
        self.fillTabs()

    def initializeTabs(self):
        for j in range(self.n*self.n):
            self.dNdKsiTab.append([])
            self.dNdEtaTab.append([])
            for i in range (0, 4):
                self.dNdKsiTab[j].append(0)
                self.dNdEtaTab[j].append(0)

    def fillTabs(self):
        for j in range(self.n*self.n):
            for i in range (0, 4):
                self.dNdKsiTab[j][i] = self.dNdKsiFunTab[i](self.points[j//self.n])
                self.dNdEtaTab[j][i] = self.dNdEtaFunTab[i](self.points[j%self.n])

    def N1(self, ksi: float, eta: float) -> float:
        return (1/4)*(1-ksi)*(1-eta)
    
    def N2(self, ksi: float, eta: float) -> float:
        return (1/4)*(1+ksi)*(1-eta)
    
    def N3(self, ksi: float, eta: float) -> float:
        return (1/4)*(1+ksi)*(1+eta)
    
    def N4(self, ksi: float, eta: float) -> float:
        return (1/4)*(1-ksi)*(1+eta)

    def dN1Ksi(self, eta: float) -> float:
        return -(1/4)*(1-eta)
    
    def dN2Ksi(self, eta: float) -> float:
        return (1/4)*(1-eta)
    
    def dN3Ksi(self, eta: float) -> float:
        return (1/4)*(1+eta)
    
    def dN4Ksi(self, eta: float) -> float:
        return -(1/4)*(1+eta)
    
    def dN1Eta(self, ksi: float) -> float:
        return -(1/4)*(1-ksi)
    
    def dN2Eta(self, ksi: float) -> float:
        return -(1/4)*(1+ksi)
    
    def dN3Eta(self, ksi: float) -> float:
        return (1/4)*(1+ksi)
    
    def dN4Eta(self, ksi: float) -> float:
        return (1/4)*(1-ksi)

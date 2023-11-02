from numerical_integration import GaussMethod
from math import *
from common import *

class UniversalElement():
    def __init__(self, n: int=2):
        self.n = n
        self.dNdKsi= []
        self.dNdEta= []
        self.dNdKsiFun = [
            self.dN1Ksi,
            self.dN2Ksi,
            self.dN3Ksi,
            self.dN4Ksi
        ]
        self.dNdEtaFun = [
            self.dN1Eta,
            self.dN2Eta,
            self.dN3Eta,
            self.dN4Eta
        ]
        self.points = []
        self.weights = []
        match self.n:
            case 1:
                self.points = [0]
                self.weights = [2]
            case 2:
                self.points = [
                    -sqrt(1/3),
                    sqrt(1/3)
                ]
                self.weights = [
                    1,
                    1
                ]
            case 3:
                self.points = [
                    -sqrt(3/5),
                    0,
                    sqrt(3/5)
                ]
                self.weights = [
                    5/9,
                    8/9,
                    5/9
                ]
            case 4:
                self.points = [
                    -sqrt(3/7 + 2/7*sqrt(6/5)),
                    -sqrt(3/7 - 2/7*sqrt(6/5)),
                    sqrt(3/7 - 2/7*sqrt(6/5)),
                    sqrt(3/7 + 2/7*sqrt(6/5))
                ]
                self.weights = [
                    
                    (18 - sqrt(30))/36,
                    (18 + sqrt(30))/36,
                    (18 + sqrt(30))/36,
                    (18 - sqrt(30))/36
                ]
            case 5:
                self.points = [
                    -(1/3)*sqrt(5 + 2*sqrt(10/7)),
                    -(1/3)*sqrt(5 - 2*sqrt(10/7)),
                    0,
                    (1/3)*sqrt(5 - 2*sqrt(10/7)),
                    (1/3)*sqrt(5 + 2*sqrt(10/7))
                ]
                self.weights = [
                    (322 - 13*sqrt(70))/900,
                    (322 + 13*sqrt(70))/900,
                    128/225,
                    (322 + 13*sqrt(70))/900,
                    (322 - 13*sqrt(70))/900
                ]
            case _:
                raise MyException("Number of nodes in numerical integration (n) must be a number in range (1;5)")
        
        self.initializeTabs()
        self.filldNdKsiTab()
        self.filldNdEtaTab()

    def initializeTabs(self):
        for j in range(self.n*self.n):
            self.dNdKsi.append([])
            self.dNdEta.append([])
            for i in range (0, 4):
                self.dNdKsi[j].append(0)
                self.dNdEta[j].append(0)

    def filldNdKsiTab(self):
        k=0
        cond = self.n-1
        for j in range(self.n*self.n):
            for i in range (0, 4):
                self.dNdKsi[j][i] = self.dNdKsiFun[i](self.points[k])
            if j == cond:
                k+=1
                cond+=self.n

    def filldNdEtaTab(self) -> None:
        k=0
        cond = self.n-1
        for j in range(self.n*self.n):
            for i in range (0, 4):
                self.dNdEta[j][i] = self.dNdEtaFun[i](self.points[k])
            if j < cond:
                k+=1
            else:
                k=0
                cond+=self.n

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

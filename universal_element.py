from numerical_integration import GaussMethod
from math import *
from common import *

class UniversalElement():
    def __init__(self, n: int=2):
        self.n = n
        self.dNKsi= []
        self.dNEta= []
        self.dNKsiFun = [
            self.dN1Ksi,
            self.dN2Ksi,
            self.dN3Ksi,
            self.dN4Ksi
        ]
        self.dNEtaFun = [
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
            
        self.fillNKsiTab()
        self.fillNEtaTab()

    def fillNKsiTab(self):
        for j in range(self.n*self.n):
            self.dNKsi.append([])
            for i in range (0, 4):
                self.dNKsi[j].append(0)
        
        k=0
        cond = self.n-1
        for j in range(self.n*self.n):
            for i in range (0, 4):
                self.dNKsi[j][i] = self.dNKsiFun[i](self.points[k])
            if j == cond:
                k+=1
                cond+=self.n

        '''
        self.dNKsi[0][0] = self.dNKsiFun[0](self.points[0])
        self.dNKsi[0][1] = self.dNKsiFun[1](self.points[0])
        self.dNKsi[0][2] = self.dNKsiFun[2](self.points[0])
        self.dNKsi[0][3] = self.dNKsiFun[3](self.points[0])
        self.dNKsi[1][0] = self.dNKsiFun[0](self.points[0])
        self.dNKsi[1][1] = self.dNKsiFun[1](self.points[0])
        self.dNKsi[1][2] = self.dNKsiFun[2](self.points[0])
        self.dNKsi[1][3] = self.dNKsiFun[3](self.points[0])
        self.dNKsi[2][0] = self.dNKsiFun[0](self.points[1])
        self.dNKsi[2][1] = self.dNKsiFun[1](self.points[1])
        self.dNKsi[2][2] = self.dNKsiFun[2](self.points[1])
        self.dNKsi[2][3] = self.dNKsiFun[3](self.points[1])
        self.dNKsi[3][0] = self.dNKsiFun[0](self.points[1])
        self.dNKsi[3][1] = self.dNKsiFun[1](self.points[1])
        self.dNKsi[3][2] = self.dNKsiFun[2](self.points[1])
        self.dNKsi[3][3] = self.dNKsiFun[3](self.points[1])
        '''
        '''
        self.dNKsi[0][0] = self.dNKsiFun[0](self.points[0])
        self.dNKsi[0][1] = self.dNKsiFun[1](self.points[0])
        self.dNKsi[0][2] = self.dNKsiFun[2](self.points[0])
        self.dNKsi[0][3] = self.dNKsiFun[3](self.points[0])
        self.dNKsi[1][0] = self.dNKsiFun[0](self.points[0])
        self.dNKsi[1][1] = self.dNKsiFun[1](self.points[0])
        self.dNKsi[1][2] = self.dNKsiFun[2](self.points[0])
        self.dNKsi[1][3] = self.dNKsiFun[3](self.points[0])
        self.dNKsi[2][0] = self.dNKsiFun[0](self.points[0])
        self.dNKsi[2][1] = self.dNKsiFun[1](self.points[0])
        self.dNKsi[2][2] = self.dNKsiFun[2](self.points[0])
        self.dNKsi[2][3] = self.dNKsiFun[3](self.points[0])
        self.dNKsi[3][0] = self.dNKsiFun[0](self.points[1])
        self.dNKsi[3][1] = self.dNKsiFun[1](self.points[1])
        self.dNKsi[3][2] = self.dNKsiFun[2](self.points[1])
        self.dNKsi[3][3] = self.dNKsiFun[3](self.points[1])
        self.dNKsi[4][0] = self.dNKsiFun[0](self.points[1])
        self.dNKsi[4][1] = self.dNKsiFun[1](self.points[1])
        self.dNKsi[4][2] = self.dNKsiFun[2](self.points[1])
        self.dNKsi[4][3] = self.dNKsiFun[3](self.points[1])
        self.dNKsi[5][0] = self.dNKsiFun[0](self.points[1])
        self.dNKsi[5][1] = self.dNKsiFun[1](self.points[1])
        self.dNKsi[5][2] = self.dNKsiFun[2](self.points[1])
        self.dNKsi[5][3] = self.dNKsiFun[3](self.points[1])
        self.dNKsi[6][0] = self.dNKsiFun[0](self.points[2])
        self.dNKsi[6][1] = self.dNKsiFun[1](self.points[2])
        self.dNKsi[6][2] = self.dNKsiFun[2](self.points[2])
        self.dNKsi[6][3] = self.dNKsiFun[3](self.points[2])
        self.dNKsi[7][0] = self.dNKsiFun[0](self.points[2])
        self.dNKsi[7][1] = self.dNKsiFun[1](self.points[2])
        self.dNKsi[7][2] = self.dNKsiFun[2](self.points[2])
        self.dNKsi[7][3] = self.dNKsiFun[3](self.points[2])
        self.dNKsi[8][0] = self.dNKsiFun[0](self.points[2])
        self.dNKsi[8][1] = self.dNKsiFun[1](self.points[2])
        self.dNKsi[8][2] = self.dNKsiFun[2](self.points[2])
        self.dNKsi[8][3] = self.dNKsiFun[3](self.points[2])
        '''

    def fillNEtaTab(self) -> None:
        for j in range(self.n*self.n):
            self.dNEta.append([])
            for i in range (0, 4):
                self.dNEta[j].append(0)

        k=0
        cond = self.n-1
        for j in range(self.n*self.n):
            for i in range (0, 4):
                self.dNEta[j][i] = self.dNEtaFun[i](self.points[k])
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

import numpy as np

from EstrategiaParticionado import EstrategiaParticionado
from Particion import Particion


class ValidacionSimple(EstrategiaParticionado):
    
    def __init__(self, porcentajeTrain):
        super().__init__()
        self.porcentajeTrain = porcentajeTrain
        self.numeroParticiones = 1
        self.nombreEstrategia = "Validación Simple"
    
    def creaParticiones(self, data):
        train = sorted(np.random.choice(len(data), len(data) * self.porcentajeTrain // 100, replace=False))
        test = list(set(range(len(data))) - set(train))
        self.particiones.append(Particion(train, test))

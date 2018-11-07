import numpy as np

from P1.EstrategiaParticionado import EstrategiaParticionado
from P1.Particion import Particion


class ValidacionSimple(EstrategiaParticionado):
    def __init__(self, porcentajeTrain):
        if 0 >= porcentajeTrain > 100:
            raise ValueError("El porcentaje tiene que estar entre 0 y 100")
        
        super().__init__()
        self.porcentajeTrain = porcentajeTrain
        self.numero_particiones = 1
        self.nombre_estrategia = "Validación Simple"
    
    def creaParticiones(self, data):
        self.particiones = []
        
        train = np.random.choice(len(data), len(data) * self.porcentajeTrain // 100, replace=False)
        test = list(set(range(len(data))) - set(train))
        self.particiones.append(Particion(train, test))

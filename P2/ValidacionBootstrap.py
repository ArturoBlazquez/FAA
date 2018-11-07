import numpy as np

from EstrategiaParticionado import EstrategiaParticionado
from Particion import Particion


class ValidacionBootstrap(EstrategiaParticionado):
    def __init__(self):
        super().__init__()
        self.numero_particiones = 1
        self.nombre_estrategia = "Validación Bootstrap"
    
    def creaParticiones(self, data):
        self.particiones = []
        
        train = np.random.choice(len(data), len(data), replace=True)
        test = list(set(range(len(data))) - set(train))
        self.particiones.append(Particion(train, test))

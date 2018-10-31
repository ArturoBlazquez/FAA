import numpy as np

from EstrategiaParticionado import EstrategiaParticionado
from Particion import Particion


class ValidacionCruzada(EstrategiaParticionado):
    def __init__(self, folds):
        super().__init__()
        self.nombre_estrategia = "Validación cruzada"
        self.numero_particiones = folds
    
    def creaParticiones(self, data):
        if self.numero_particiones > len(data):
            raise ValueError("Hay más folds que datos")
        
        self.particiones = []
        
        indices = np.arange(len(data))
        np.random.shuffle(indices)
        indices_particiones = split(indices, self.numero_particiones)
        
        for indices_test in indices_particiones:
            train = list(set(range(len(data))) - set(indices_test))
            test = list(indices_test)
            
            self.particiones.append(Particion(train, test))


def split(seq, num):
    k, m = divmod(len(seq), num)
    return (seq[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(num))

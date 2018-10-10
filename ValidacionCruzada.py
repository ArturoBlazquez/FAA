import numpy as np

import EstrategiaParticionado
from Particion import Particion


# TODO: testear que funciona
class ValidacionCruzada(EstrategiaParticionado):

    def __init__(self, folds):
        self.nombre_estrategia = "Validación cruzada"
        self.numero_particiones = folds

    def creaParticiones(self, data):
        indices = np.arange(len(data))
        np.random.shuffle(indices)
        particiones = split(indices, self.numero_particiones)

        for particion in particiones:
            train = list(set(range(len(data))) - set(particion))
            test = particion

            self.particiones.append(Particion(train, test))


def split(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

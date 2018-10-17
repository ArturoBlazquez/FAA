#Para que haga Nico :)

import EstrategiaParticionado
import numpy as np
from Particion import Particion

class ValidacionSimple(EstrategiaParticionado):

    def __init__(self, porcentajeTrain):
        self.porcentajeTrain = porcentajeTrain
        self.numeroParticiones = 1
        self.nombreEstrategia = "Validación Simple"

    def creaParticiones(self, data):
        train = sorted(np.random.choice(len(data), len(indices) * self.porcentajeTrain // 100, replace=False))
        test = list(set(range(len(data))) - set(train))
        Particion(train,test)
    # TODO: chequear si esta bien el return out
        return out


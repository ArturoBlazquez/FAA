#Para que haga Nico :)

import EstrategiaParticionado
import numpy as np
from Particion import Particion


class ValidacionSimple(EstrategiaParticionado):


    def __init__(self, porcentajeTrain):
        self.porcentajeTrain=porcentajeTrain
        self.numeroParticiones=1
        self.nombreEstrategia="Validación Simple"

    def creaParticiones(self, data):
        indices =np.arange(len(data))
        desordenados = np.random.shuffle(indices)

        indexDivision= len(data)*self.porcentajeTrain//100
        train = desordenados[:indexDivision]
        test = desordenados[indexDivision:]
        Particion(train,test)



        np.random.choice(len(data),self.porcentajeTrain,replace=False)
        return


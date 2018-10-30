import numpy as np
from abc import ABCMeta, abstractmethod


class Clasificador(metaclass=ABCMeta):
    def __init__(self):
        pass
    
    @abstractmethod
    def entrenamiento(self, datosTrain, atributosDiscretos, diccionario):
        pass
    
    @abstractmethod
    def clasifica(self, datosTest, atributosDiscretos, diccionario):
        pass
    
    def error(self, datos, pred):
        return datos[:, -1] != pred
    
    def validacion(self, particionado, dataset, clasificador, seed=None):
        particionado.creaParticiones(dataset.datos)

        errores= []

        for particion in particionado.particiones:
            atributosDiscretos = dataset.nominalAtributos
            diccionario = dataset.diccionarios

            clasificador.entrenamiento(dataset.extraeDatos(particion.indicesTrain), atributosDiscretos, diccionario)
            pred = clasificador.clasifica(dataset.extraeDatos(particion.indicesTest), atributosDiscretos, diccionario)

            errores.append(self.error(dataset.extraeDatos(particion.indicesTest), pred))

        return np.array(errores).flatten()

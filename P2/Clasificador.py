import itertools
from abc import ABCMeta, abstractmethod

import numpy as np


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
    
    def validacion(self, particionado, dataset, clasificador, seed=None, aplicar_correccion_de_laplace=True):
        particionado.creaParticiones(dataset.datos)
        
        errores = []
        
        for particion in particionado.particiones:
            datos_train = dataset.extraeDatos(particion.indicesTrain)
            datos_test = dataset.extraeDatos(particion.indicesTest)
            atributosDiscretos = dataset.nominalAtributos
            diccionario = dataset.diccionarios
            
            clasificador.entrenamiento(datos_train, atributosDiscretos, diccionario, aplicar_correccion_de_laplace)
            pred = clasificador.clasifica(datos_test, atributosDiscretos, diccionario)
            
            errores.append(self.error(datos_test, pred))
        
        errores = list(itertools.chain.from_iterable(errores))
        
        tasa_de_error = sum(errores) / len(errores)
        
        return errores, tasa_de_error
    
    def calcularMediasDesv(self, datos_train, atributosDiscretos):
        medias = []
        desviaciones = []
        for i, is_discreto in enumerate(atributosDiscretos):
            if is_discreto:
                medias.append(0)
                desviaciones.append(1)
            else:
                medias.append(np.mean(datos_train[:, i]))
                desviaciones.append(np.std(datos_train[:, i]))
        
        return medias, desviaciones
    
    def normalizarDatos(self, datos, medias, desviaciones):
        np.ndarray()
    

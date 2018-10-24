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
    
    # TODO: implementar
    def error(self, datos, pred):
        pass
    
    # TODO: implementar
    def validacion(self, particionado, dataset, clasificador, seed=None):
        pass

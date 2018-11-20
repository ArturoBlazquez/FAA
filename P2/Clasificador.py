import itertools
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
    
    def validacion(self, particionado, dataset, clasificador, seed=None, normalizar_datos=None, nepocas=None):
        particionado.creaParticiones(dataset.datos)
        
        errores = []
        
        for particion in particionado.particiones:
            datos_train = dataset.extraeDatos(particion.indicesTrain)
            datos_test = dataset.extraeDatos(particion.indicesTest)
            atributosDiscretos = dataset.nominalAtributos
            diccionario = dataset.diccionarios
            
            if normalizar_datos is not None:
                clasificador.entrenamiento(datos_train, atributosDiscretos, diccionario, normalizar_datos)
            elif nepocas is not None:
                clasificador.entrenamiento(datos_train, atributosDiscretos, diccionario, nepocas)
            else:
                clasificador.entrenamiento(datos_train, atributosDiscretos, diccionario)
            
            pred = clasificador.clasifica(datos_test[:, :-1], atributosDiscretos, diccionario)
            
            errores.append(self.error(datos_test, pred))
        
        errores = list(itertools.chain.from_iterable(errores))
        
        tasa_de_error = sum(errores) / len(errores)
        
        return errores, tasa_de_error

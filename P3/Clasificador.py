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
    
    def validacion(self, particionado, dataset, clasificador, num_generaciones=None, num_individuos=None):
        particionado.creaParticiones(dataset.datos)
        
        errores = []
        
        for particion in particionado.particiones:
            datos_train = dataset.extraeDatos(particion.indicesTrain)
            datos_test = dataset.extraeDatos(particion.indicesTest)
            atributosDiscretos = dataset.nominalAtributos
            diccionario = dataset.diccionarios
            
            if num_generaciones is None or num_individuos is None:
                clasificador.entrenamiento(datos_train, atributosDiscretos, diccionario)
            else:
                clasificador.entrenamiento(datos_train, atributosDiscretos, diccionario,
                                           num_generaciones=num_generaciones, num_individuos=num_individuos)
            
            pred = clasificador.clasifica(datos_test[:, :-1], atributosDiscretos, diccionario)
            
            errores.append(self.error(datos_test, pred))
        
        errores = list(itertools.chain.from_iterable(errores))
        
        tasa_de_error = sum(errores) / len(errores)
        
        return errores, tasa_de_error

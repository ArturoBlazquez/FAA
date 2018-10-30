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
        aciertos = 0
        fallos = 0
        
        for is_acierto in (datos[:, -1] == pred):
            if is_acierto:
                aciertos += 1
            else:
                fallos += 1
        
        return aciertos, fallos
    
    def validacion(self, particionado, dataset, clasificador, seed=None):
        particionado.creaParticiones(dataset.datos)
        
        for particion in particionado.particiones:
            atributosDiscretos = dataset.nominalAtributos
            diccionario = dataset.diccionarios
            
            clasificador.entrenamiento(dataset.extraeDatos(particion.indicesTrain), atributosDiscretos, diccionario)
            pred = clasificador.clasifica(dataset.extraeDatos(particion.indicesTest), atributosDiscretos, diccionario)
            
            aciertos, fallos = self.error(dataset.extraeDatos(particion.indicesTest), pred)
            
            print(aciertos * 100 / (aciertos + fallos), "% de aciertos", sep='')
            print(fallos * 100 / (aciertos + fallos), "% de fallos", sep='')

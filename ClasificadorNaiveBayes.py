import numpy as np

from Clasificador import Clasificador


class ClasificadorNaiveBayes(Clasificador):
    def __init__(self):
        super().__init__()
        self.tables = []
    
    def entrenamiento(self, datosTrain, atributosDiscretos, diccionario, aplicar_correccion_de_laplace=True):
        for i, is_discreto in enumerate(atributosDiscretos[:-1]):
            if is_discreto:
                table = np.zeros((len(diccionario[i]), len(diccionario[-1])))
                
                for data in datosTrain:
                    table[int(data[i]), int(data[-1])] += 1
                
                self.tables.append(table)
            
            else:
                mean = np.mean(datosTrain[:, i])
                var = np.var(datosTrain[:, i])
                
                self.tables.append([mean, var])
    
    def clasifica(self, datosTest, atributosDiscretos, diccionario):
        pass

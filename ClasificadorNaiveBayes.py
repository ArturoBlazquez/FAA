import numpy as np

from Clasificador import Clasificador


class ClasificadorNaiveBayes(Clasificador):
    def __init__(self):
        super().__init__()
        self.tables = []
    
    def entrenamiento(self, datosTrain, atributosDiscretos, diccionario, aplicar_correccion_de_laplace=True):
        for i, is_discreto in enumerate(atributosDiscretos[:]):
            if is_discreto:
                table = np.zeros((len(diccionario[i]), len(diccionario[-1])))
                
                for data in datosTrain:
                    table[int(data[i]), int(data[-1])] += 1
                
                if i < len(atributosDiscretos) - 1:
                    if aplicar_correccion_de_laplace and has_any_zeros(table):
                        table = table + 1
                    
                    for column in np.transpose(table):
                        column /= sum(column)
                
                self.tables.append(table)
            
            else:
                # TODO: comprobar que la media y la varianza están bien
                table = np.zeros((2, len(diccionario[-1])))
                datos_agrupados = [[] for i in range(len(diccionario[-1]))]
                
                for data in datosTrain:
                    datos_agrupados[int(data[-1])].append(data[i])
                
                for j, grupo in enumerate(datos_agrupados):
                    mean = np.mean(grupo)
                    var = np.var(grupo)
                    table[:, j] = [mean, var]
                
                self.tables.append(table)
    
    def clasifica(self, datosTest, atributosDiscretos, diccionario):
        for row in datosTest:
            probabilidades = []
            
            for clase in range(len(diccionario[-1])):
                prob = 1
                for i, is_discreto in enumerate(atributosDiscretos[:]):
                    if is_discreto:
                        if i < len(atributosDiscretos) - 1:
                            prob *= self.tables[i]


def has_any_zeros(table):
    return np.size(table) - np.count_nonzero(table) != 0

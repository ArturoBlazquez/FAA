import math

import numpy as np

from P1.Clasificador import Clasificador


class ClasificadorNaiveBayes(Clasificador):
    def __init__(self):
        super().__init__()
        self.tables = []
    
    def entrenamiento(self, datosTrain, atributosDiscretos, diccionario, aplicar_correccion_de_laplace=True):
        self.tables = []
        
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
        
        clasificacion = []
        
        for row in datosTest:
            probabilidades = []
            
            for clase in range(len(diccionario[-1])):
                prob = 1
                for i, is_discreto in enumerate(atributosDiscretos[:]):
                    if i < len(atributosDiscretos) - 1:
                        atrib_table = self.tables[i]
                        data = int(row[i])
                        
                        if is_discreto:
                            prob *= atrib_table[data, clase]
                        else:
                            mean = atrib_table[0, clase]
                            var = atrib_table[1, clase]
                            prob *= (1 / math.sqrt(2 * math.pi * var)) * math.exp((-(data - mean) ** 2) / (2 * var))
                    else:
                        prob *= self.tables[i][clase, clase]
                
                probabilidades.append(prob)
            
            clasificacion.append(probabilidades.index(max(probabilidades)))
        
        return np.array(clasificacion)


def has_any_zeros(table):
    return np.size(table) - np.count_nonzero(table) != 0

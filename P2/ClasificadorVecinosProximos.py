import math

import numpy as np

from Clasificador import Clasificador


class ClasificadorVecinosProximos(Clasificador):
    def __init__(self, k):
        super().__init__()
        self.desviaciones = []
        self.medias = []
        self.datos = []
        self.k = k
    
    def entrenamiento(self, datosTrain, atributosDiscretos, diccionario):
        self.__init__(self.k)
        
        self.medias, self.desviaciones = Clasificador.calcularMediasDesv(datosTrain, atributosDiscretos)
        self.datos = Clasificador.normalizarDatos(datosTrain, self.medias, self.desviaciones)
    
    def clasifica(self, datosTest, atributosDiscretos, diccionario):
        datos_a_clasificar = Clasificador.normalizarDatos(datosTest, self.medias, self.desviaciones)
        
        clasificacion = []
        
        for dato_a_clasificar in datos_a_clasificar:
            distancias = []
            for dato in self.datos:
                d = calcular_distancia(dato_a_clasificar, dato, atributosDiscretos)
                distancias.append(d)
            
            indices_vecinos = np.argpartition(np.array(distancias), self.k)
            
            clase_vecinos = self.datos[indices_vecinos, -1]
            
            clasificacion.append(clase_mas_frecuente(clase_vecinos))
        
        return np.array(clasificacion)


def calcular_distancia(dato1, dato2, atributosDiscretos):
    distancias = []
    
    for i, is_discreto in enumerate(atributosDiscretos):
        if is_discreto:
            if dato1[i] == dato2[i]:
                distancias.append(0)
            else:
                distancias.append(1)
        else:
            distancias.append((dato1[i] - dato2[i]) ** 2)  # distancia euclídea sin tomar la raíz
    
    return math.sqrt(sum(distancias))


def clase_mas_frecuente(lst):
    return max(set(lst), key=lst.count)

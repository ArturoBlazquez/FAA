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
    
    def entrenamiento(self, datosTrain, atributosDiscretos, diccionario, normalizar_datos=True):
        self.__init__(self.k)
        
        if normalizar_datos:
            self.medias, self.desviaciones = calcularMediasDesv(datosTrain[:, :-1], atributosDiscretos[:-1])
            datos = normalizarDatos(datosTrain[:, :-1], self.medias, self.desviaciones)
            
            self.datos = np.column_stack((datos, datosTrain[:, -1]))
        else:
            self.medias = [0 for _ in atributosDiscretos]
            self.desviaciones = [1 for _ in atributosDiscretos]
            self.datos = datosTrain
    
    def clasifica(self, datosTest, atributosDiscretos, diccionario):
        datos_a_clasificar = normalizarDatos(datosTest, self.medias, self.desviaciones)
        
        clasificacion = []
        
        for dato_a_clasificar in datos_a_clasificar:
            distancias = []
            for dato in self.datos:
                d = calcular_distancia(dato_a_clasificar, dato[:-1], atributosDiscretos[:-1])
                distancias.append(d)
            
            indices_vecinos = np.argpartition(distancias, self.k)[:self.k]
            
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
    (values, counts) = np.unique(lst, return_counts=True)
    ind = np.argmax(counts)
    return values[ind]


def calcularMediasDesv(datos_train, atributosDiscretos):
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


def normalizarDatos(datos, medias, desviaciones):
    datos_normalizados = np.empty_like(datos)
    
    for i, dato in enumerate(datos):
        for j in range(len(medias)):
            media = medias[j]
            desviacion = desviaciones[j]
            
            datos_normalizados[i, j] = (dato[j] - media) / desviacion
    
    return datos_normalizados

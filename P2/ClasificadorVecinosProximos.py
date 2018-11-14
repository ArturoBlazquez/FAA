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
        
        self.medias, self.desviaciones = calcularMediasDesv(datosTrain, atributosDiscretos)
        self.datos = normalizarDatos(datosTrain, self.medias, self.desviaciones)
    
    def clasifica(self, datosTest, atributosDiscretos, diccionario):
        datos_a_clasificar = normalizarDatos(datosTest, self.medias, self.desviaciones)
        
        clasificacion = []
        
        for dato_a_clasificar in datos_a_clasificar:
            distancias = []
            for dato in self.datos:
                d = calcular_distancia(dato_a_clasificar[:-1], dato[:-1], atributosDiscretos[:-1])
                distancias.append(d)
            
            indices_vecinos = np.argsort(distancias)[:self.k]
            
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
    return values[ind]  # prints the most frequent element


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

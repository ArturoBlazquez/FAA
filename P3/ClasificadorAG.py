from random import randint, getrandbits

import numpy as np

from Clasificador import Clasificador


class ClasificadorAG(Clasificador):
    REPRESENTACION_ENTERA = 0
    REPRESENTACION_BINARIA = 1
    
    def __init__(self):
        super().__init__()
    
    def entrenamiento(self, datosTrain, atributosDiscretos, diccionario, representacion=REPRESENTACION_ENTERA,
                      numero_de_individuos=100, numero_de_generaciones=100, min_reglas=1, max_reglas=100,
                      probabilidad_de_mutacion=1):
        self.__init__()
        
        k = 5
        
        individuos = genera_poblacion_inicial(numero_de_individuos, min_reglas, max_reglas, len(atributosDiscretos), k,
                                              representacion)
        
        for i in range(numero_de_generaciones):
            fitness = calcula_fitness(individuos, representacion, datosTrain)
            
            hijos = recombinacion(individuos, fitness)
            
            hijos_mutados = mutacion(hijos, probabilidad_de_mutacion)
            
            individuos = seleccion_de_supervivientes(individuos, hijos_mutados)
    
    def clasifica(self, datosTest, atributosDiscretos, diccionario):
        clasificacion = []
        
        return np.array(clasificacion)


def genera_poblacion_inicial(numero_de_individuos, min_reglas, max_reglas, num_atributos, k, representacion):
    individuos = []
    
    for i in range(numero_de_individuos):
        individuo = []
        num_reglas = randint(min_reglas, max_reglas)
        
        for j in range(num_reglas):
            if representacion == ClasificadorAG.REPRESENTACION_ENTERA:
                regla = [randint(0, k) for _ in range(num_atributos - 1)] + [randint(0, 1)]
            elif representacion == ClasificadorAG.REPRESENTACION_BINARIA:
                regla = [getrandbits(k) for _ in range(num_atributos - 1)] + [randint(0, 1)]
            
            individuo.append(regla)
        
        individuos.append(individuo)
    
    return individuos


def calcula_fitness(individuos, tipo_de_representacion, datosTrain):
    return [1, 2, 3]


def recombinacion(individuos, fitness):
    hijos = []
    
    for i in range(len(individuos) / 2):
        padre1 = selecciona_padre(individuos, fitness)
        padre2 = selecciona_padre(individuos, fitness)
        
        hijo1, hijo2 = cruce(padre1, padre2)
        
        hijos.append(hijo1)
        hijos.append(hijo2)
    
    return hijos


def selecciona_padre(individuos, fitness):
    #TODO


#TODO: ver tipos de representacion
def cruce(ind1, ind2):
    '''Cruce de dos individuos para devolver los hijos'''
    # Numero aleatorio para el cruce entre 1 y el tamanio del menor individuo
    cruce_index = randint(1, min(len(ind1), len(ind2)))
    hijo1 = ind1[:cruce_index] + ind2[cruce_index:]
    hijo2 = ind2[:cruce_index] + ind1[cruce_index:]
    return hijo1, hijo2


def mutacion(hijos, probabilidad_de_mutacion):
    return [1, 2, 3]


def seleccion_de_supervivientes(individuos, hijos):
    return [1, 2, 3]

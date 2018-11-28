from random import randint

import numpy as np

from Clasificador import Clasificador


class ClasificadorAG(Clasificador):
    def __init__(self):
        super().__init__()
    
    def entrenamiento(self, datosTrain, atributosDiscretos, diccionario, tipo_de_representacion=0,
                      numero_de_individuos=100, numero_de_generaciones=100, min_reglas=1, max_reglas=100,
                      probabilidad_de_mutacion=1, k=5):
        self.__init__()
        
        individuos = genera_poblacion_inicial(100, min_reglas, max_reglas, len(atributosDiscretos), k)
        
        for i in range(100):
            fitness = calcula_fitness(individuos, tipo_de_representacion, datosTrain)
            
            hijos = recombinacion(individuos, fitness)
            
            hijos_mutados = mutacion(hijos, probabilidad_de_mutacion)
            
            individuos = seleccion_de_supervivientes(individuos, hijos_mutados)
    
    def clasifica(self, datosTest, atributosDiscretos, diccionario):
        clasificacion = []
        
        return np.array(clasificacion)


def genera_poblacion_inicial(numero_de_individuos, min_reglas, max_reglas, num_atributos, k):
    individuos = []
    
    for i in range(numero_de_individuos):
        individuo = []
        num_reglas = randint(min_reglas, max_reglas)
        
        for j in range(num_reglas):
            regla = [randint(0, k) for _ in range(num_atributos - 1)] + [randint(0, 1)]
            individuo.append(regla)
        
        individuos.append(individuo)
    
    return individuos


def calcula_fitness(individuos, tipo_de_representacion, datosTrain):
    return [1, 2, 3]


def recombinacion(individuos, fitness):
    return [1, 2, 3]


def mutacion(hijos, probabilidad_de_mutacion):
    return [1, 2, 3]


def seleccion_de_supervivientes(individuos, hijos):
    return [1, 2, 3]

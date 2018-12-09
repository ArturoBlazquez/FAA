from math import log10
from random import randint, getrandbits, random

import numpy as np

from Clasificador import Clasificador

REPRESENTACION_ENTERA = 0
REPRESENTACION_BINARIA = 1

CRUCE_DE_REGLAS = 0
CRUCE_INTER_REGLAS = 1

MUTACION_SIMPLE = 0
MUTACION_PORCENTAJE_DE_INDIVIDUOS = 1


class ClasificadorAG(Clasificador):
    def __init__(self, k):
        self.k = k
        super().__init__()
    
    def entrenamiento(self, datosTrain, atributosDiscretos, diccionario, num_individuos=100, min_reglas=1,
                      max_reglas=100, representacion=REPRESENTACION_ENTERA, num_generaciones=100,
                      tipo_cruce=CRUCE_INTER_REGLAS, tipo_mutacion=MUTACION_SIMPLE, prob_mutacion=0.01):
        k = int(1 + 3.322 * log10(len(datosTrain)))
        self.__init__(k)
        num_atributos = len(atributosDiscretos) - 1
        apriori = max(set(datosTrain[-1]), key=datosTrain[-1].count)
        
        individuos = genera_poblacion_inicial(num_individuos, min_reglas, max_reglas, num_atributos, k, representacion)
        
        for i in range(num_generaciones):
            fitness = calcula_fitness(individuos, discretiza(datosTrain, k), representacion, apriori)
            
            hijos = recombinacion(individuos, fitness, tipo_cruce)
            
            mutacion(hijos, prob_mutacion, k, representacion, tipo_mutacion)
            
            individuos = seleccion_de_supervivientes(individuos, hijos)
    
    def clasifica(self, datosTest, atributosDiscretos, diccionario):
        clasificacion = []
        
        return np.array(clasificacion)


def genera_poblacion_inicial(num_individuos, min_reglas, max_reglas, num_atributos, k, representacion):
    individuos = []
    
    for i in range(num_individuos):
        individuo = []
        num_reglas = randint(min_reglas, max_reglas)
        
        for j in range(num_reglas):
            if representacion == REPRESENTACION_ENTERA:
                regla = [randint(0, k) for _ in range(num_atributos)] + [randint(0, 1)]
            elif representacion == REPRESENTACION_BINARIA:
                regla = [getrandbits(k) for _ in range(num_atributos)] + [randint(0, 1)]
            
            individuo.append(regla)
        
        individuos.append(individuo)
    
    return individuos


def discretiza(datos, k):
    datos_discretos = np.empty_like(datos)
    
    for j in range(datos.shape[1]):
        x_min = min(datos[:, j])
        x_max = max(datos[:, j])
        
        a = (x_max - x_min) / k
        
        for i in range(datos.shape[0]):
            
            x_0 = x_min
            for intervalo in range(1, k + 1):
                if x_0 <= datos[i, j] <= x_0 + a:
                    datos_discretos[i, j] = intervalo
                    break
                else:
                    x_0 = x_0 + a
    
    return datos_discretos


def calcula_fitness(individuos, datos, representacion, apriori):
    fitness = []
    
    for individuo in individuos:
        aciertos = 0
        for dato in datos:
            if devuelve_clase(individuo, dato, representacion, apriori) == dato[-1]:
                aciertos += 1
        fitness.append(aciertos)
    
    return fitness


def devuelve_clase(individuo, dato, representacion, apriori):
    clasificacion = []
    
    for regla in individuo:
        clasificacion.append(devuelve_clase_regla(regla, dato, representacion))
    
    num_clase0 = clasificacion.count(0)
    num_clase1 = clasificacion.count(1)
    
    if num_clase0 == num_clase1:
        return apriori
    elif num_clase0 > num_clase1:
        return 0
    elif num_clase0 < num_clase1:
        return 1


def devuelve_clase_regla(regla, dato, representacion):
    if representacion == REPRESENTACION_ENTERA:
        for i, gen in enumerate(regla[:-1]):
            if gen != 0 and gen != dato[i]:
                return
        return regla[-1]
    elif representacion == REPRESENTACION_BINARIA:
        for i, gen in enumerate(regla[:-1]):
            if gen != 0 and (gen & dato[i]) != dato[i]:
                return
        return regla[-1]


def recombinacion(individuos, fitness, tipo_cruce):
    hijos = []
    
    for i in range(len(individuos) // 2):
        padre1 = selecciona_padre(individuos, fitness)
        padre2 = selecciona_padre(individuos, fitness)
        
        hijo1, hijo2 = cruce(padre1, padre2, tipo_cruce)
        
        hijos += hijo1, hijo2
    
    return hijos


def selecciona_padre(individuos, fitness):
    fitness_total = sum(fitness)
    probabilidad_de_seleccion = [f / fitness_total for f in fitness]
    
    indice_padre = np.random.choice(len(individuos), p=probabilidad_de_seleccion)
    
    return individuos[indice_padre]


def cruce(ind1, ind2, tipo_cruce):
    if tipo_cruce == CRUCE_INTER_REGLAS:
        num_atributos = len(ind1[0])
        cruce_index = randint(1, min(len(ind1), len(ind2)) * num_atributos - 1)
        
        regla_index = cruce_index // num_atributos
        inter_index = cruce_index - regla_index * num_atributos
        
        regla_del_medio = [ind1[regla_index][0:inter_index] + ind2[regla_index][inter_index:]]
        hijo1 = ind1[:regla_index] + regla_del_medio + ind2[regla_index + 1:]
        
        regla_del_medio = [ind2[regla_index][0:inter_index] + ind1[regla_index][inter_index:]]
        hijo2 = ind2[:regla_index] + regla_del_medio + ind1[regla_index + 1:]
    elif tipo_cruce == CRUCE_DE_REGLAS:
        cruce_index = randint(1, min(len(ind1), len(ind2)))
        
        hijo1 = ind1[:cruce_index] + ind2[cruce_index:]
        hijo2 = ind2[:cruce_index] + ind1[cruce_index:]
    
    return hijo1, hijo2


def mutacion(individuos, prob_mutacion, k, representacion, tipo_mutacion):
    if tipo_mutacion == MUTACION_SIMPLE:
        for i, individuo in enumerate(individuos):
            for r, regla in enumerate(individuo):
                for g, gen in enumerate(regla):
                    if random() < prob_mutacion:
                        if representacion == REPRESENTACION_ENTERA:
                            individuos[i][r][g] = randint(0, k)
                        elif representacion == REPRESENTACION_BINARIA:
                            individuos[i][r][g] = getrandbits(k)


def seleccion_de_supervivientes(individuos, hijos):
    return individuos[:2] + hijos[2:]

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
    def __init__(self, k=0):
        self.k = k
        self.individuo = []
        self.stats = []
        super().__init__()
    
    def entrenamiento(self, datosTrain, atributosDiscretos, diccionario, num_individuos=100, min_reglas=1,
                      max_reglas=4, representacion=REPRESENTACION_ENTERA, tasa_ceros=0.9, num_generaciones=100,
                      tipo_cruce=CRUCE_INTER_REGLAS, tipo_mutacion=MUTACION_SIMPLE, prob_mutacion=0.001):
        k = int(1 + 3.322 * log10(len(datosTrain)))
        self.__init__(k)
        num_atributos = len(atributosDiscretos) - 1
        apriori = clase_mas_frecuente(datosTrain[:, -1])
        
        individuos = genera_poblacion_inicial(num_individuos, min_reglas, max_reglas, num_atributos, k, representacion,
                                              tasa_ceros)
        
        for i in range(num_generaciones):
            fitness = calcula_fitness(individuos, discretiza(datosTrain, k), representacion, apriori)
            self.update_stats(individuos, fitness)
            
            hijos = recombinacion(individuos, fitness, tipo_cruce)
            
            mutacion(hijos, prob_mutacion, k, representacion, tipo_mutacion)
            
            individuos = seleccion_de_supervivientes(individuos, hijos)
        
        fitness = calcula_fitness(individuos, discretiza(datosTrain, k), representacion, apriori)
        self.update_stats(individuos, fitness)
        self.stats.append(calcula_fitness([[]], datosTrain, representacion, apriori)[0])  # Append apriori fitness
        
        self.individuo = self.stats[-2][1]
    
    def clasifica(self, datosTest, atributosDiscretos, diccionario):
        clasificacion = []
        
        return np.array(clasificacion)
    
    def update_stats(self, individuos, fitness):
        mejor_individuo = individuos[fitness.index(max(fitness))]
        fitness_medio = sum(fitness) / len(individuos)
        
        self.stats.append([fitness_medio, mejor_individuo, max(fitness)])


def genera_poblacion_inicial(num_individuos, min_reglas, max_reglas, num_atributos, k, representacion, tasa_ceros):
    individuos = []
    
    for i in range(num_individuos):
        individuo = []
        num_reglas = randint(min_reglas, max_reglas)
        
        for j in range(num_reglas):
            if representacion == REPRESENTACION_ENTERA:
                regla = [randint(0, k) for _ in range(num_atributos)] + [randint(0, 1)]
            elif representacion == REPRESENTACION_BINARIA:
                regla = [getrandbits(k) for _ in range(num_atributos)] + [randint(0, 1)]
            
            while regla.count(0) / num_atributos < tasa_ceros:
                regla[randint(0, num_atributos)] = 0
            individuo.append(regla)
        
        individuos.append(individuo)
    
    return individuos


def discretiza(datos, k):
    datos_discretos = np.copy(datos)
    
    for j in range(datos.shape[1] - 1):
        x_min = min(datos[:, j])
        x_max = max(datos[:, j])
        
        a = (x_max - x_min) / k
        
        for i in range(datos.shape[0]):
            intervalo = datos[i, j] // a
            datos_discretos[i, j] = np.clip(intervalo, 1, k)
    
    return datos_discretos


def calcula_fitness(individuos, datos, representacion, apriori):
    fitness = []
    
    for individuo in individuos:
        aciertos = 0
        for dato in datos:
            if devuelve_clase(individuo, dato, representacion, apriori) == dato[-1]:
                aciertos += 1
        fitness.append(aciertos)
    
    # Si el fitness de TODOS los individuos es 0, asignamos un valor positivo para poder hacer cruces
    if max(fitness) == 0:
        for i in range(len(fitness)):
            fitness[i] = 1
    
    # Devolvemos la tasa de aciertos
    num_datos = len(datos)
    return [f / num_datos for f in fitness]


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
            if gen != 0 and (gen & int(dato[i])) != dato[i]:
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
                        if g == len(regla) - 1:
                            individuos[i][r][g] = randint(0, 1)
                        elif representacion == REPRESENTACION_ENTERA:
                            individuos[i][r][g] = randint(0, k)
                        elif representacion == REPRESENTACION_BINARIA:
                            individuos[i][r][g] = getrandbits(k)


def seleccion_de_supervivientes(individuos, hijos):
    return individuos[:10] + hijos[10:]


def clase_mas_frecuente(lst):
    (values, counts) = np.unique(lst, return_counts=True)
    ind = np.argmax(counts)
    return values[ind]

import random

def cruce(ind1, ind2):
    '''Cruce de dos individuos para devolver los hijos'''
    # Numero aleatorio para el cruce entre 1 y el tamanio del menor individuo
    cruce_index = random.randint(1, min(len(ind1),len(ind2)))
    hijo1 = ind1[:cruce_index]+ind2[cruce_index:]
    hijo2 = ind2[:cruce_index]+ind1[cruce_index:]
    return hijo1, hijo2


def mutacion(ind,k):
    '''Mutacion dentro de una de las reglas del individuo'''
    regla_index = random.randint(0, len(ind)-1)
    intra_regla_index = random.randint(0, len(ind[regla_index])-1)
    valor_mutado = random.randint(0, k)
    ind_mutado = ind
    ind_mutado[regla_index][intra_regla_index] = valor_mutado
    return ind_mutado

def calcula_fitness(individuos, datos, representacion, apriori):
    '''devuelve array con el fitness de cada individuo'''
    fitness = []
    for individuo in individuos:
        aciertos = 0
        for dato in datos:
            if devuelve_clase(individuo, dato, representacion, apriori) == dato[-1]
                aciertos += 1
        fitness.append(aciertos)
    return fitness

def devuelve_clase(individuo, dato, representacion, apriori):
    '''devuelve la clase con la que clasifica a un dato segun las reglas de un individuo'''
    clasificacion = []
    for regla in individuo:
        clasificacion.append(devuelve_clase_regla(regla, dato, representacion))
    # replace None with apriori
    num_clase0 = clasificacion.count(0)
    num_clase1 = clasificacion.count(1)
    if num_clase0 == num_clase1:
        return apriori
    elif num_clase0 > num_clase1:
        return 0
    elif num_clase0 < num_clase1:
        return 1


def devuelve_clase_regla(regla, dato, representacion):
    '''devuelve la clase con la que una regla clasifica a un dato, o devuelve None si no
    clasifica'''
    # TODO: considerar la representacion binaria
    for gen,i in enumerate(regla[:-1]):
        if gen != 0 and gen != dato[i]: # and (gen & dato[i]) != dato[i]:
            return
    return regla[-1]

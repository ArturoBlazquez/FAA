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

from Datos import Datos
from sklearn.linear_model import LogisticRegression
from ValidacionBootstrap import ValidacionBootstrap
from ValidacionCruzada import ValidacionCruzada
from ValidacionSimple import ValidacionSimple
import numpy as np


# TODO: corroborar y completar
# https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

example1 = Datos('ConjuntosDatos/example1.data')

validaciones = [ValidacionSimple(70), ValidacionCruzada(6), ValidacionBootstrap()]

validaciones[0].creaParticiones(example1.datos)

# TODO: normalizar los datos (usando funciones de sklearn o nuestra?)

X = np.zeros((len(validaciones[0].particiones[0].indicesTest),len(example1.nominalAtributos)-1))
# ndarray para los datos de test que no incluye la clase
y = np.zeros((len(validaciones[0].particiones[0].indicesTest),1)) # ndarray para las clases

# Completo ndarrays X e y
for n, indiceTest in enumerate(validaciones[0].particiones[0].indicesTest):
    X[n]=example1.datos[indiceTest,:-1]
    y[n] =example1.datos[indiceTest,-1]

algoritmo = 'sag'    # Es el que recomienda el profesor SAG = Stochastic Average Gradient
pesoClase = 'balanced'

# Clasificador Regresion Logistica de sklearn
SK_RegLog = LogisticRegression(class_weight=pesoClase , solver=algoritmo,
                               multi_class='auto').fit(X, y) # ver si hay que cambiar penalty
# (creo que es el eta), tol (tolerance) y max_iter

# clasifica todos los datos de example.datos y los guarda en predicho
predicho=[]
for dat in example1.datos:
    predicho.append(SK_KNN.predict([dat[:-1]]))

# TODO: error del modelo (tomarlo de Arturo). Comparar 'predicho' con 'y'

verdadero=0
falso=0
for i in range(len(y)):
    if y[i] == predicho[i]:
        verdadero +=1
    else:
        falso +=1

print (verdadero , "," , falso)

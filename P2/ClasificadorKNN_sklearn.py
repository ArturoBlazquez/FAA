from Datos import Datos
from ValidacionSimple import ValidacionSimple
from sklearn.neighbors import KNeighborsClassifier
from ValidacionBootstrap import ValidacionBootstrap
from ValidacionCruzada import ValidacionCruzada
from ValidacionSimple import ValidacionSimple
import numpy as np

# del ejemplo sacado de internet
# X = [[0], [1], [2], [3]]   # Vectores de datos (datos train)
# y = [0, 0, 1, 1]           # Clases de los vectores (de datos train)

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

k = 3    # Probar con diferentes valores de k
peso = 'uniform'  # Probar tambien con 'distance'

# Clasificador KNN de sklearn
SK_KNN = KNeighborsClassifier(n_neighbors=k, weights=peso)
SK_KNN.fit(X, y)

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

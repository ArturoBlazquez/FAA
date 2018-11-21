from Datos import Datos
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from ValidacionSimple import ValidacionSimple
import numpy as np
import itertools

conjuntos_de_datos = ['example1', 'example2', 'example3', 'example4', 'wdbc']
val = ValidacionSimple(70)
valores_de_k = [1, 3, 5, 11, 21, 51]
pesos = ['uniform', 'distance']

for peso in pesos:
    print ("\nPeso =", peso)
    for nombre_fichero in conjuntos_de_datos:
        datos = Datos('ConjuntosDatos/' + nombre_fichero + '.data')
        val.creaParticiones(datos.datos) #Se usa Validacion Simple

        # Normalizo los datos
        datos_normalizados = preprocessing.normalize(datos.datos, axis=0)
        datos_normalizados[:,-1] = datos.datos[:,-1]

        # ndarray para los datos de test que no incluye la clase
        X = np.zeros((len(val.particiones[0].indicesTrain),len(datos.nominalAtributos)-1))
        y = []
        # Completo ndarrays X e y
        for n, indiceTrain in enumerate(val.particiones[0].indicesTrain):
            X[n]=datos_normalizados[indiceTrain,:-1]
            y.append(datos_normalizados[indiceTrain,-1])

        print(nombre_fichero, ":", sep='')
        for k in valores_de_k:
            SK_KNN = KNeighborsClassifier(n_neighbors=k, weights=peso)    # Clasificador KNN de sklearn
            SK_KNN.fit(X, y)    # Ingreso los Datos al modelo

            # clasifica todos los datos de datos.datos y los guarda en predicho
            predicho=[]
            for dato in datos_normalizados:
                predicho.append(SK_KNN.predict([dato[:-1]]))

            # errores para los datos de Test y tasa de error correspondiente
            errores = []
            for n, indiceTest in enumerate(val.particiones[0].indicesTest):
                errores.append(datos_normalizados[indiceTest,-1] != predicho[indiceTest])
            errores = list(itertools.chain.from_iterable(errores))
            tasa_de_error = sum(errores) / len(errores)

            print("\tTasa de error: k=", k, ":\t\t", tasa_de_error, sep='')

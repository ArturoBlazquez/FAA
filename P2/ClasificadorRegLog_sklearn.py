from Datos import Datos
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from ValidacionSimple import ValidacionSimple
import numpy as np
import itertools

conjuntos_de_datos = ['example1', 'example2', 'example3', 'example4', 'wdbc']
val = ValidacionSimple(70)
algoritmo = 'sag'    # Usaremos SAG = Stochastic Average Gradient
pesoClase = 'balanced'

nrosepocas = [1,5,10,100]
constantes = [0.4,0.6,0.8,1.0]


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

    for constante in constantes:
        for nepocas in nrosepocas:
            SK_RegLog = LogisticRegression(C=constante, class_weight=pesoClase , solver=algoritmo,
                               multi_class='auto', max_iter=nepocas) # Clasificador RegLog de
            # sklearn - ver si
            #  hay que cambiar penalty (constante eta), tol (tolerance) y max_iter
            SK_RegLog.fit(X, y)

            # clasifica todos los datos de datos.datos y los guarda en predicho
            predicho=[]
            for dato in datos_normalizados:
                predicho.append(SK_RegLog.predict([dato[:-1]]))

            # errores para los datos de Test y tasa de error correspondiente
            errores = []
            for n, indiceTest in enumerate(val.particiones[0].indicesTest):
                errores.append(datos_normalizados[indiceTest,-1] != predicho[indiceTest])
            errores = list(itertools.chain.from_iterable(errores))
            tasa_de_error = sum(errores) / len(errores)

            print("\tTasa de error const=", constante, ", nepocas=", nepocas, ":\t\t", tasa_de_error, sep='')

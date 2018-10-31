import itertools

from sklearn import preprocessing
from sklearn.model_selection import train_test_split, KFold
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from Datos import Datos

# Los datos a analizar con SKlearn son german.data y tic-tac-toe.data
dataset = Datos('ConjuntosDatos/german.data')

# Encode categorical integer features using a one-hot aka one-of-K scheme (categorical features). Hay DeprecationWarnings
encAtributos = preprocessing.OneHotEncoder(categorical_features=dataset.nominalAtributos[:-1], sparse=False)
X = encAtributos.fit_transform(dataset.datos[:,:-1])

# Clases correspondientes a cada uno de los array de X
y = dataset.datos[:,-1]


# particiones --> entrenamiento (fit) --> clasificar (predict) --> error
# Particiones del modo Validacion Simple
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Entrenamiento y clasificacion de X_test
gnb = GaussianNB()
y_pred = gnb.fit(X_train, y_train).predict(X_test)

errores = y_pred != y_test
tasa_de_error = sum(errores)/len(errores)

print(tasa_de_error)


# Particiones del modo Validacion Cruzada
# KFold(n_splits=’warn’, shuffle=False, random_state=None)

kf = KFold(n_splits=6, shuffle=True)

errores=[]
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    y_pred = gnb.fit(X_train, y_train).predict(X_test)

    errores.append(y_pred != y_test)

errores = list(itertools.chain.from_iterable(errores))
tasa_de_error = sum(errores) / len(errores)
print(tasa_de_error)

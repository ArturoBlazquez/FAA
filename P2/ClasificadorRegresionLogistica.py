import numpy as np
from scipy.special import expit as sigmoidal

from Clasificador import Clasificador


class ClasificadorRegresionLogistica(Clasificador):
    def __init__(self):
        super().__init__()
        self.w = []
    
    def entrenamiento(self, datosTrain, atributosDiscretos, diccionario, nepocas=10, const=0.78):
        self.__init__()
        
        w = np.random.uniform(-0.5, 0.5, len(atributosDiscretos))
        
        for i in range(nepocas):
            for data in datosTrain:
                x = np.append(1, data[:-1])
                sigma = sigmoidal(np.matmul(w, x))
                
                w = w - const * (sigma - data[-1]) * x
        
        self.w = w
    
    def clasifica(self, datosTest, atributosDiscretos, diccionario):
        clasificacion = []
        
        for dato in datosTest:
            x = np.append(1, dato)
            a = np.matmul(self.w, x)
            
            if a > 0:
                clasificacion.append(1.0)
            else:
                clasificacion.append(0.0)
        
        return np.array(clasificacion)

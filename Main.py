import unittest

from Datos import Datos

"""
TODO:
      - Dos clases: clasificadores y particionado
      - Particionado guarda una lista de particiones
        - Partición guarda sólo los índices y no los datos como tal
        - Extrae datos de una lista de índices me devuelve la matriz correspondiente
      - Entrenadores:
        - error y validación son métodos generales
          - Validación extrae los datos de train y luego extrae los datos de test y clasifica.
            Luego llama al error y calcula la tasa.
        - Luego cada clasificador tiene sus propios métodos
      
      - Tenemos 4 semanas para hacer toda esta movida
      
      Crear modelo:
      discreto -> en NB el modelo es el conjunto de probabilidades de las clases, etc. Entrenamiento hace las tablas
      continuo -> Calcular media y desviación al entrenar.
      
      Clasifica:
        - Uso las tablas
      
      Error:
        Compara la clase que nos da clasifica con la real
        
      Corrección de Laplace:
        Vamos a ver si tiene algún efecto sobre los conjuntos que estamos analizando
        
        
        Para la parte 3 podemos hacer sciky.py o hacer un clasificador clasificadorsci.py
        
        
        
      Entregar: Datos, clasificador, estartegiaparticion, clasificadornb
"""


class DatosTest(unittest.TestCase):
    def test_datos_init(self):
        balloons = Datos('ConjuntosDatos/balloons.data')
        tic_tac_toe = Datos('ConjuntosDatos/tic-tac-toe.data')
        german = Datos('ConjuntosDatos/german.data')
        
        self.assertIsInstance(balloons, Datos)
        self.assertIsInstance(tic_tac_toe, Datos)
        self.assertIsInstance(german, Datos)
        
        with self.assertRaisesRegex(ValueError, Datos.ERROR_DIFERENTE_NUMERO_ATRIBUTOS_Y_TIPOS):
            Datos('ConjuntosDatos/unitTests/diferente_numero_atributos_y_tipos.data')
        
        with self.assertRaisesRegex(ValueError, Datos.ERROR_DIFERENTE_NUMERO_DATOS):
            Datos('ConjuntosDatos/unitTests/diferente_numero_datos.data')
        
        with self.assertRaisesRegex(ValueError, Datos.ERROR_TIPO_NO_CONTINUO_NI_NOMINAL):
            Datos('ConjuntosDatos/unitTests/tipo_atributos_no_continuo_ni_nominal.data')
        
        with self.assertRaises(FileNotFoundError):
            Datos('ConjuntosDatos/unitTests/no_existe.data')


if __name__ == '__main__':
    unittest.main()

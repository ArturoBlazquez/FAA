import unittest

from Datos import Datos


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

# -*- coding: utf-8 -*-
import numpy as np

class Datos(object):
    TiposDeAtributos=('Continuo','Nominal')

    def __init__(self, nombreFichero):
        with open(nombreFichero) as f:
            lines = f.readlines();

            self.nombreAtributos = lines[1].strip().split(',')
            self.tipoAtributos = lines[2].strip().split(',')

            if set(self.tipoAtributos).difference(set(self.TiposDeAtributos)):
                raise ValueError('Hay datos que no son {0[0]} ni {0[1]}'.format(self.TiposDeAtributos))

            if len(self.nombreAtributos) != len(self.tipoAtributos):
                raise ValueError('No coincide el número de atributos en las filas 2 y 3')

            self.nombreAtributos = lines[1].strip().split(',')

        nombreAtributos
        tipoAtributos
        nominalAtributos
        datos
        diccionarios


    # TODO: implementar en la pr�ctica 1
    def extraeDatos(idx):
        pass

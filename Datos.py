# -*- coding: utf-8 -*-
import numpy as np


class Datos(object):
    TiposDeAtributos = ('Continuo', 'Nominal')

    def __init__(self, nombre_fichero):
        with open(nombre_fichero) as f:
            lines = f.readlines()

            self.nombreAtributos = lines[1].strip().split(',')
            self.tipoAtributos = lines[2].strip().split(',')

            if set(self.tipoAtributos).difference(set(self.TiposDeAtributos)):
                raise ValueError('Hay datos que no son {0[0]} ni {0[1]}'.format(self.TiposDeAtributos))

            if len(self.nombreAtributos) != len(self.tipoAtributos):
                raise ValueError('No coincide el número de atributos en las filas 2 y 3')

            self.nominalAtributos = np.array(self.tipoAtributos) == "Nominal"

            datos_sin_procesar = np.array([line.strip().split(',') for line in lines[3:]])

            self.diccionarios = []
            self.datos = np.zeros((int(lines[0].strip()), len(self.nombreAtributos)), dtype=int)

            for i, nominal in enumerate(self.nominalAtributos):
                if nominal:
                    nombres_de_atributos = sorted(set(datos_sin_procesar[:, i]))
                    self.diccionarios.append({v: k for k, v in enumerate(nombres_de_atributos)})

                    self.datos[:, i] = [self.diccionarios[-1][data] for data in datos_sin_procesar[:, i]]
                else:
                    self.diccionarios.append({})

                    self.datos[:, i] = datos_sin_procesar[:, i]

    # TODO: implementar en la práctica 1
    def extrae_datos(self, idx):
        pass

from abc import ABCMeta, abstractmethod


class EstrategiaParticionado(metaclass=ABCMeta):
    nombre_estrategia = ""
    numero_particiones = 0
    particiones = []

    @abstractmethod
    def crea_particiones(self):
        pass

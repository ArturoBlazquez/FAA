from abc import ABCMeta, abstractmethod


class EstrategiaParticionado(metaclass=ABCMeta):
    def __init__(self):
        self.nombre_estrategia = ""
        self.numero_particiones = 0
        self.particiones = []
    
    @abstractmethod
    def creaParticiones(self, data):
        pass

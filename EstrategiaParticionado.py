from abc import ABCMeta, abstractmethod


class EstrategiaParticionado(metaclass=ABCMeta):
    def __init__(self):
        self.nombre_estrategia = ""
        self.numero_particiones = 0
        self.particiones = []
    
    # TODO: control de errores si pasas porcentaje negativo o 150% o número de folds raros
    # TODO: meter la seed
    @abstractmethod
    def creaParticiones(self, data):
        pass

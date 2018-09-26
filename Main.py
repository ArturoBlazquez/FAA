from Datos import Datos

balloons = Datos('<datasets-home>/balloons.data')
tic_tac_toe = Datos('<datasets-home>/tic-tac-toe.data')
german = Datos('<datasets-home>/german.data')

assert isinstance(balloons, Datos)
assert isinstance(tic_tac_toe, Datos)
assert isinstance(german, Datos)

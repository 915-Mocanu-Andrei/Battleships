from Battleships.domain.entities import *


class SRepo:
    def __init__(self):
        self._ships=[]

    def add(self,ship):
        self._ships.append(ship)

    def get_ships(self):
        return self._ships

    def get_functional_ships(self):
        f_ships=[]
        for i in self._ships:
            if i.status == 1:
                f_ships.append(i)
        return f_ships

    def get_destroyed_ships(self):
        f_ships=[]
        for i in self._ships:
            if i.status == 0:
                f_ships.append(i)
        return f_ships

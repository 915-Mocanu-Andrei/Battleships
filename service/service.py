from Battleships.domain.entities import *
from random import randint
import copy


class Service:
    def __init__(self,map_repo,ships_repo):
        self._map_repo = map_repo
        self._ships_repo = ships_repo

    def position_ship(self, line, column, orientation, length):
        ship = self.create_ship_body(line, column, orientation, length)
        response = self.check_for_overwriting(ship)
        if response != 1:
            self._ships_repo.add(ship)
            for i in ship.cells:
                self._map_repo.change_cell_status(i[0], i[1], 1)
        return response

    def create_ship_body(self,line,column,orientation,length):
        cells = []
        if orientation == "h":
            for i in range(int(column), int(column) + length):
                tuple=(int(line),int(i))
                cells.append(tuple)
        if orientation == "v":
            for i in range(line, line+length):
                tuple=(int(i),int(column))
                cells.append(tuple)
        ship = Ship(1, length, cells, 0)
        ship.cells=cells
        return ship

    def check_for_overwriting(self,ship):
        response = 0
        for i in ship.cells:
            if i[0] < 10 and i[1] < 10:
                if 1 == self._map_repo.get_cell_status(i[0],i[1]):
                    response = 1
            else:
                response = 1
        return response

    def column_to_int(self,column):
        return(ord(column) - ord('a'))

    def attack(self,line,column):
        """
        :param line: integer representing line
        :param column: integer representing column
        :return: modifies the attacked ship and the map
        """
        self.attack_map(line,column)
        a = self.attack_ship(line,column)
        return a

    def attack_map(self,line,column):
        """
        :param line: integer representing line
        :param column: integer representing column
        :return: marks the spot in the repository
        """
        # 0 means empty
        # 1 means part of a functional ship
        # 2 means miss
        # 3 means hit
        if self._map_repo.get_cell_status(line, column) == 0:
            self._map_repo.change_cell_status(line, column , 2)
        if self._map_repo.get_cell_status(line, column) == 1:
            self._map_repo.change_cell_status(line, column, 3)

    def attack_ship(self,line,column):
        """
                :param line: integer representing line
                :param column: integer representing column
                :return: increases marks of a ship that is attacked,changes its status if that's the case
                """
        for ship in self._ships_repo.get_functional_ships():
            tuple = (line, column)
            if tuple in ship.cells:
                ship.marks = ship.marks +1
                if ship.marks == ship.length:
                    ship.status=0
                    return ship.length
        return 0

    def check_defeat(self):
        """
        :return: checks for defeat
        """
        defeat = 1
        for i in range(0,9):
            for j in range(0,9):
                if self._map_repo.get_cell_status(i,j) == 1:
                    defeat = 0
        return defeat

    def get_map(self):
        return self._map_repo.get_repo()


class Ai:
    def __init__(self):
        self._i = -1
        self._shots= []
        self._hits = 0
        self._length = 2
        self._orientation = 'v'
        self._cells_to_hit = []
        self._enemy_map =[]

    def get_enemy_map(self, enemy_map):
        self._enemy_map = copy.deepcopy(enemy_map)

    def placing_ships(self):
        ":return: random ship coordinates"
        r = randint(1,2)
        if r == 1:
            self._orientation = 'v'
        if r == 2:
            self._orientation = 'h'
        tuple = (randint(0,9),randint(0,9),self._orientation)
        return tuple

    def get_random_cell(self):#returns random cell
        l = randint(1, 10-self._length)
        c = randint(1, 10-self._length)
        tup = (l, c)
        return tup

    def get_ai_attack(self):
        self._i = self._i + 1
        print(self._i)
        return self._shots[self._i]

    def hit(self):
        if len(self._cells_to_hit) == 0:
            self._cells_to_hit.append((randint(0, 9), randint(0, 9)))
        else:
            cell = self._cells_to_hit[-1]
            if cell in self._shots:
                pass
            self._shots.append(cell)
            self._cells_to_hit = self._cells_to_hit[:-1]
            if self._enemy_map[cell[0]][cell[1]] == 1:
                self._enemy_map[cell[0]][cell[1]] = 2
                if cell[0] > 0:
                    self.hit_up((cell[0]-1, cell[1]))
                if cell[0] < 9:
                    self.hit_down((cell[0] + 1, cell[1]))
                if cell[1] > 0:
                    self.hit_left((cell[0], cell[1]-1))
                if cell[1] < 9:
                    self.hit_right((cell[0], cell[1]+1))
                self._hits = self._hits+1
        if self._hits >= 2+3+3+4+5:
            return 1
        else:
            return 0

    def hit_up(self, cell):
        if cell in self._shots:
            pass
        self._shots.append(cell)
        if self._enemy_map[cell[0]][cell[1]] == 1 :
            self._enemy_map[cell[0]][cell[1]] = 2
            if cell[0] > 0:
                self.hit_up((cell[0]-1, cell[1]))
            self._hits = self._hits + 1
        if 0 <= cell[1]-1 <= 9:
            self._cells_to_hit.append((cell[0], cell[1]-1))
        if 0 <= cell[1] + 1 <= 9:
            self._cells_to_hit.append((cell[0], cell[1]+1))

    def hit_down(self, cell):
        if cell in self._shots:
            pass
        self._shots.append(cell)
        if self._enemy_map[cell[0]][cell[1]] == 1:
            self._enemy_map[cell[0]][cell[1]] = 2
            if cell[0] < 9:
                self.hit_down((cell[0] + 1, cell[1]))
            self._hits = self._hits + 1
        if 0 <= cell[1] - 1 <= 9:
            self._cells_to_hit.append((cell[0], cell[1] - 1))
        if 0 <= cell[1] + 1 <= 9:
            self._cells_to_hit.append((cell[0], cell[1] + 1))

    def hit_left(self, cell):
        if cell in self._shots:
            pass
        self._shots.append(cell)
        if self._enemy_map[cell[0]][cell[1]] == 1 :
            self._enemy_map[cell[0]][cell[1]] = 2
            if cell[1] > 0:
                self.hit_left((cell[0], cell[1]-1))
            self._hits = self._hits + 1
        if 0 <= cell[0]-1 <= 9:
            self._cells_to_hit.append((cell[0]-1, cell[1] ))
        if 0 <= cell[0] + 1 <= 9:
            self._cells_to_hit.append((cell[0]+1, cell[1] ))

    def hit_right(self, cell):
        if cell in self._shots:
            pass
        self._shots.append(cell)
        if self._enemy_map[cell[0]][cell[1]] == 1 :
            self._enemy_map[cell[0]][cell[1]] = 2
            if cell[1] < 9:
                self.hit_right((cell[0], cell[1]+1))
            self._hits = self._hits + 1
        if 0 <= cell[0] - 1 <= 9:
            self._cells_to_hit.append((cell[0] - 1, cell[1]))
        if 0 <= cell[0] + 1 <= 9:
            self._cells_to_hit.append((cell[0] + 1, cell[1]))



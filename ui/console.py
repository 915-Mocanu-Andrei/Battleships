from Battleships.service.service import *
from Battleships.repository.ships_repo import *
from Battleships.repository.map_repo import *


class Console:
    def __init__(self, service1, service2):
        self._service1 = service1
        self._service2 = service2
        self._ai = Ai()
        self.W = '\033[0m'  # white (normal)
        self.R = '\033[31m'  # red --Hit
        self.G = '\033[32m'  # green --Ship
        self.O = '\033[33m'  # orange
        self.B = '\033[34m'  # blue
        self.P = '\033[35m'  # purple
        self.cheat = False

    def start(self):
        print("Welcome to Battleships!\n"
              "To play this game you first need to place your ships on the board.\n"
              "Choose the cells in which you want to place your ships.\n"
              "First choose a cell(a1/c6/f3), then an orientation(h/v)\n"
              "Do you want to play vs 1.AI or 2.Human")
        ai_human = int(input('='))
        print("Do you want to cheat? 0=No or 1=Yes")
        self.cheat = bool(int(input('=')))
        self.placement(ai_human)
        self.battle(ai_human)

    def placement(self, ai_human):
        self.placement_1()
        if ai_human == 1:
            self.placement_ai()
        if ai_human == 2:
            self.placement_2()

    def placement_ai(self):
        response = 1
        while response == 1:
            tup = self._ai.placing_ships()
            response = self._service2.position_ship(tup[0], tup[1], tup[2], 2)
        response = 1
        while response == 1:
            tup = self._ai.placing_ships()
            response = self._service2.position_ship(tup[0], tup[1], tup[2], 3)
        response = 1
        while response == 1:
            tup = self._ai.placing_ships()
            response = self._service2.position_ship(tup[0], tup[1], tup[2], 3)
        response = 1
        while response == 1:
            tup = self._ai.placing_ships()
            response = self._service2.position_ship(tup[0], tup[1], tup[2], 4)
        response = 1
        while response == 1:
            tup = self._ai.placing_ships()
            response = self._service2.position_ship(tup[0], tup[1], tup[2], 5)

    def placement_1(self):
        input("Player1:Press Enter?")
        self.print_map(1, True)
        self.player_placement(1, 2, 1)
        self.player_placement(2, 3, 1)
        self.player_placement(3, 3, 1)
        self.player_placement(4, 4, 1)
        self.player_placement(5, 5, 1)

    def placement_2(self):
        input("Player2:Press Enter?")
        self.print_map(2, True)
        self.player_placement(1, 2, 2)
        self.player_placement(2, 3, 2)
        self.player_placement(3, 3, 2)
        self.player_placement(4, 4, 2)
        self.player_placement(5, 5, 2)

    def print_map(self, map, see_ships=True):
        service = self._service1.get_map()
        if map == 2:
            service = self._service2.get_map()
        print(end='  ')
        lineLetter = 'A'
        for i in range(10):
            print(lineLetter, end=' ')
            lineLetter = chr(ord(lineLetter) + 1)
        print('')
        columnNr = 1
        for line in service:
            print(columnNr, end=' ')
            columnNr = columnNr + 1
            for cell in line:
                if cell == 0:
                    print(self.W, end='')
                    print(cell, end=' ')
                    print(self.W, end='')
                if cell == 1:
                    if see_ships:
                        print(self.G, end='')
                        print(cell, end=' ')
                    else:
                        # If the player isn't cheating he can't see the ships'
                        print(self.W, end='')
                        print(0, end=' ')
                    print(self.W, end='')
                if cell == 2:
                    print(self.B, end='')
                    print(cell, end=' ')
                    print(self.W, end='')
                if cell == 3:
                    print(self.R, end='')
                    print(cell, end=' ')
                    print(self.W, end='')
            print('')

    def player_placement(self, ship_nr, length, player):
        response = 1
        while response == 1:
            print("Ship", ship_nr, ", length", length)
            start_cell = str(input('start_cell='))
            orientation = str(input('orientation='))
            if len(start_cell) == 3:
                a = start_cell[0]
                del start_cell
                start_cell = [a, 10]
            if player == 1:
                response = self._service1.position_ship(int(start_cell[1]) - 1,
                                                        self._service1.column_to_int(start_cell[0]), orientation,
                                                        length)
                self.print_map(1, True)
            if player == 2:
                response = self._service2.position_ship(int(start_cell[1]) - 1,
                                                        self._service2.column_to_int(start_cell[0]), orientation,
                                                        length)
                self.print_map(2, True)
            if response == 1:
                print("Can't place it there!\n")

    def battle(self, ai_human):
        defeat = 0
        if ai_human == 1:
            self.ai_get_ready()
            while defeat == 0:
                print("Player1 turn")
                self.print_map(1, True)
                print('')
                self.print_map(2, self.cheat)
                print('')
                self.player_attack(1)
                self.ai_attack()
                if self._service2.check_defeat() == 1:
                    defeat = 1
                if self._service1.check_defeat() == 1:
                    defeat = 2
        if ai_human == 2:
            while defeat == 0:
                input("Player1 turn")
                self.print_map(1, True)
                print('')
                self.print_map(2, False)
                self.player_attack(1)

                input("Player2 turn")
                self.print_map(2, True)
                print('')
                self.print_map(1, False)
                self.player_attack(2)
                if self._service2.check_defeat() == 1:
                    defeat = 1
                if self._service1.check_defeat() == 1:
                    defeat = 2
        if defeat == 0:
            self.battle(ai_human)
        if defeat == 1:
            print("Player 1 wins!")
        if defeat == 2:
            print("Player 2 wins!")

    def player_attack(self, player):
        cell = str(input("Cell to attack:"))
        if len(cell) == 3:
            a = cell[0]
            del cell
            cell = [a, 10]
        if player == 1:
            a = self._service2.attack(int(cell[1]) - 1, self._service1.column_to_int(cell[0]))
            if a != 0:
                print(str(("Ship destroyed! ") + str(a) + "Length"))
        if player == 2:
            a = self._service1.attack(int(cell[1]) - 1, self._service2.column_to_int(cell[0]))
            if a != 0:
                print(str(("Ship destroyed! ") + str(a) + "Length"))

    def ai_attack(self):
        tuple = self._ai.get_ai_attack()
        a = self._service1.attack(tuple[0], tuple[1])
        if a != 0:
            print(str(("Ship destroyed! ") + str(a) + "Length"))

    def ai_get_ready(self):
        self._ai.get_enemy_map(self._service1.get_map())
        a = self._ai.hit()
        while a == 0:
            a = self._ai.hit()

from Battleships.ui.console import *

import unittest


class Testing(unittest.TestCase):

    def setUp(self):
        self.m1 = MRepo()
        self.m2 = MRepo()
        self.s1 = SRepo()
        self.s2 = SRepo()
        self.ser1 = Service(self.m1, self.s1)
        self.ser2 = Service(self.m2, self.s2)
        self.ser1.position_ship(4,4,'v',3)
        self.ai = Ai()
        self.ai._enemy_map=[[0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,1,0,0,0,0,0,0],
                      [0,0,0,1,0,0,0,1,0,0],
                      [0,0,0,1,0,0,0,1,0,0],
                      [0,0,0,0,0,0,0,1,0,0],
                      [0,0,0,0,0,0,0,1,0,0],
                      [0,0,0,1,1,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0]]

    def test_position_ship(self):
        self.ser1.position_ship(1, 2, 'h', 2)
        self.assertEqual(self.m1.get_cell_status(1, 2), 1)

    def test_attack(self):
        self.ser1.position_ship(1, 2, 'h', 2)
        self.ser1.attack(1,2)
        self.assertEqual(self.m1.get_cell_status(1,2),3)

    def test_attack_miss(self):
        self.ser1.attack(1, 2)
        self.assertEqual(self.m1.get_cell_status(1, 2), 2)

    def test_check_defeat(self):
        self.assertEqual(self.ser1.check_defeat(),0)

    def test_ai(self):
        self.ai.placing_ships()
        self.ai.get_enemy_map(self.m1)
        a = self.ai.hit()
        b = self.ai.get_random_cell()
        self.assertEqual(1,1)

    def test_ai_placing_ships(self):
        self.ai.placing_ships()

    def test_ai_hit(self):
        a = self.ai.hit()
        while a == 0:
            a= self.ai.hit()
        self.assertEqual(a,1)

    def test_get_destroyed_ships(self):
        ship = Ship(0, 2, [(2,2), (2, 3)], 4)
        self.s1.add(ship)
        self.assertEqual(len(self.s1.get_destroyed_ships()),1)

    def test_get_ships(self):
        ship = Ship(0, 2, [(2, 2), (2, 3)], 0)
        self.s1.add(ship)
        ship2 = Ship(1, 3, [(2, 2), (2, 3), (2, 4)], 0)
        self.s1.add(ship2)
        ships = self.s1.get_ships()
        self.assertTrue(len(ships) == 3)

    def test_ai_get_enemy_map(self):
        self.ai.get_enemy_map(self.m1)

if __name__ == "__main__":
    unittest.main()

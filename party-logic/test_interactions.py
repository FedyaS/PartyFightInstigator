import unittest
from interactions import average_out, compound, interact
from person import Person

class TestInteractions(unittest.TestCase):
    def test_average_out_strength_1(self):
        v1, v2 = average_out(80, 20, 1)
        self.assertEqual(v1, 50)
        self.assertEqual(v2, 50)

    def test_average_out_strength_05(self):
        v1, v2 = average_out(80, 20, 0.5)
        self.assertEqual(v1, 65)
        self.assertEqual(v2, 35)

    def test_average_out_strength_0(self):
        v1, v2 = average_out(80, 20, 0)
        self.assertEqual(v1, 80)
        self.assertEqual(v2, 20)

    def test_compound_strength_1(self):
        v1, v2 = compound(10, 20, 1)
        self.assertEqual(v1, 30)  # 10 + 20
        self.assertEqual(v2, 30)  # 20 + 10

    def test_compound_strength_05(self):
        v1, v2 = compound(10, 20, 0.5)
        self.assertEqual(v1, 20)  # 10 + (1/2)*20 = 10+10 = 20
        self.assertEqual(v2, 25)  # 20 + (1/2)*10 = 20+ 5 = 25

    def test_compound_strength_0(self):
        v1, v2 = compound(10, 20, 0)
        self.assertEqual(v1, 10)
        self.assertEqual(v2, 20)

    def test_interact(self):
        p1 = Person()
        p2 = Person()
        p1.ES.set_emotional_state(joy=80, anger=10, anxiety=30, jealousy=5, curiosity=90)
        p2.ES.set_emotional_state(joy=20, anger=20, anxiety=10, jealousy=15, curiosity=10)

        interact(p1, p2, strength=1)

        self.assertEqual(p1.ES.joy, 50)
        self.assertEqual(p2.ES.joy, 50)
        self.assertEqual(p1.ES.anxiety, 20)
        self.assertEqual(p2.ES.anxiety, 20)
        self.assertEqual(p1.ES.anger, 30)   # 10 + 20
        self.assertEqual(p2.ES.anger, 30)   # 20 + 10
        self.assertEqual(p1.ES.jealousy, 20)
        self.assertEqual(p2.ES.jealousy, 20)
        self.assertEqual(p1.ES.curiosity, 50)
        self.assertEqual(p2.ES.curiosity, 50)

if __name__ == '__main__':
    unittest.main()

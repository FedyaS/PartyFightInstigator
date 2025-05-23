# import pytest
# from simulation.interactions import average_out, compound, interact
# from simulation.person import Person
#
# def test_average_out_strength_1():
#     v1, v2 = average_out(80, 20, 1)
#     assert v1 == 50
#     assert v2 == 50
#
# def test_average_out_strength_05():
#     v1, v2 = average_out(80, 20, 0.5)
#     assert v1 == 65
#     assert v2 == 35
#
# def test_average_out_strength_0():
#     v1, v2 = average_out(80, 20, 0)
#     assert v1 == 80
#     assert v2 == 20
#
# def test_compound_strength_1():
#     v1, v2 = compound(10, 20, 1)
#     assert v1 == 30  # 10 + 20
#     assert v2 == 30  # 20 + 10
#
# def test_compound_strength_05():
#     v1, v2 = compound(10, 20, 0.5)
#     assert v1 == 20  # 10 + (1/2)*20 = 10+10 = 20
#     assert v2 == 25  # 20 + (1/2)*10 = 20+ 5 = 25
#
# def test_compound_strength_0():
#     v1, v2 = compound(10, 20, 0)
#     assert v1 == 10
#     assert v2 == 20
#
# def test_interact():
#     p1 = Person()
#     p2 = Person()
#     p1.ES.set_emotional_state(joy=80, anger=10, anxiety=30, jealousy=5, curiosity=90)
#     p2.ES.set_emotional_state(joy=20, anger=20, anxiety=10, jealousy=15, curiosity=10)
#
#     interact(p1, p2, strength=1)
#
#     assert p1.ES.joy == 50
#     assert p2.ES.joy == 50
#     assert p1.ES.anxiety == 20
#     assert p2.ES.anxiety == 20
#     assert p1.ES.anger == 30   # 10 + 20
#     assert p2.ES.anger == 30   # 20 + 10
#     assert p1.ES.jealousy == 20
#     assert p2.ES.jealousy == 20
#     assert p1.ES.curiosity == 50
#     assert p2.ES.curiosity == 50

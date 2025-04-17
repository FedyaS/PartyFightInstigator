import unittest
from relationships import RelationshipManager, Relationship
from person import Person

class TestRelationshipManager(unittest.TestCase):

    def setUp(self):
        self.rm = RelationshipManager()
        self.p1 = Person(name="Alice")
        self.p2 = Person(name="Bob")
        self.p3 = Person(name="Claire")

    def test_set_and_get_relationship(self):
        self.rm.set_relationship(self.p1, self.p2, trust=80, resentment=10)
        rel = self.rm.get_relationship(self.p1, self.p2)
        self.assertIsNotNone(rel)
        self.assertEqual(rel.trust, 80)
        self.assertEqual(rel.resentment, 10)

    def test_update_existing_relationship(self):
        self.rm.set_relationship(self.p1, self.p2, trust=60, resentment=5)
        self.rm.update_relationship(self.p1, self.p2, trust=70)
        rel = self.rm.get_relationship(self.p1, self.p2)
        self.assertEqual(rel.trust, 70)
        self.assertEqual(rel.resentment, 5)

    def test_update_nonexistent_relationship(self):
        self.rm.update_relationship(self.p1, self.p2, trust=90, resentment=20)
        rel = self.rm.get_relationship(self.p1, self.p2)
        self.assertIsNotNone(rel)
        self.assertEqual(rel.trust, 90)
        self.assertEqual(rel.resentment, 20)

    def test_get_outgoing_relationships(self):
        self.rm.set_relationship(self.p1, self.p2, trust=55)
        self.rm.set_relationship(self.p1, self.p3, trust=45)
        self.rm.set_relationship(self.p2, self.p1, trust=20)

        outgoing = self.rm.get_outgoing_relationships(self.p1)
        self.assertEqual(len(outgoing), 2)
        self.assertIn(self.p2.id, outgoing)
        self.assertIn(self.p3.id, outgoing)
        self.assertNotIn(self.p1.id, outgoing)

    def test_init_all_relationships(self):
        people = [self.p1, self.p2, self.p3]
        self.rm.init_all_relationships(people, trust=60, resentment=15)
        self.assertEqual(len(self.rm.relations), 6)
        self.assertIsNotNone(self.rm.get_relationship(self.p1, self.p2))
        self.assertIsNotNone(self.rm.get_relationship(self.p2, self.p1))
        self.assertEqual(self.rm.get_relationship(self.p1, self.p2).trust, 60)
        self.assertEqual(self.rm.get_relationship(self.p1, self.p2).resentment, 15)

    def test_init_all_relationships_with_randomization(self):
        people = [self.p1, self.p2, self.p3]
        trust_base = 70
        resentment_base = 10
        radius = 10
        self.rm.init_all_relationships(people, trust=trust_base, resentment=resentment_base, randomize_range=radius)

        for rel in self.rm.relations.values():
            print(rel.trust, rel.resentment)
            self.assertTrue(trust_base - radius <= rel.trust <= trust_base + radius)
            self.assertTrue(resentment_base - radius <= rel.resentment <= resentment_base + radius)

if __name__ == '__main__':
    unittest.main()

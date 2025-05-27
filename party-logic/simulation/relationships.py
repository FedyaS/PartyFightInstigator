from simulation.utils import apply_random_modifier
from simulation.person import Person

class Relationship:
    def __init__(self, person1: Person, person2: Person, trust=500, animosity=0, randomize_stats=0):
        # Sort persons by ID to ensure consistent ordering
        sorted_persons = sorted([person1, person2], key=lambda p: p.id)
        self.person1 = sorted_persons[0]  # Lower ID
        self.person2 = sorted_persons[1]  # Higher ID
        self.id = (self.person1.id, self.person2.id)
        self.trust = apply_random_modifier(trust, randomize_stats)
        self.animosity = apply_random_modifier(animosity, randomize_stats)
from person import Person
from utils import apply_random_modifier

class Relationship:
    def __init__(self, trust=50, resentment=0):
        self.trust = trust
        self.resentment = resentment

class RelationshipManager:
    # (person1.id, person2.id) → person1's view of person2
    def __init__(self):
        self.relations = {}  # key: tuple of (id1, id2), value: Relationship object

    def _key(self, id1, id2):
        return (id1, id2)

    def set_relationship(self, p1: Person, p2: Person, trust=50, resentment=0):
        self.relations[self._key(p1.id, p2.id)] = Relationship(trust, resentment)

    def get_relationship(self, p1: Person, p2: Person):
        return self.relations.get(self._key(p1.id, p2.id), None)

    def update_relationship(self, p1: Person, p2: Person, trust=None, resentment=None):
        rel = self.get_relationship(p1, p2)
        if rel:
            if trust is not None:
                rel.trust = trust
            if resentment is not None:
                rel.resentment = resentment
        else:
            self.set_relationship(p1, p2, trust or 50, resentment or 0)

    def get_outgoing_relationships(self, person):
        """Here's how this person feels about others."""
        return {
            id2: rel
            for (id1, id2), rel in self.relations.items()
            if id1 == person.id
        }
    
    def init_all_relationships(self, people: list[Person], trust=50, resentment=0, randomize_range=0):
        for p1 in people:
            for p2 in people:
                if p1.id != p2.id:
                    my_trust = apply_random_modifier(trust, randomize_range) if randomize_range else trust
                    my_resentment = apply_random_modifier(resentment, randomize_range) if randomize_range else resentment
                    self.set_relationship(p1, p2, trust=my_trust, resentment=my_resentment)


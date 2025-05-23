import pytest
from simulation.relationships import RelationshipManager, Relationship
from simulation.person import Person

@pytest.fixture
def relationship_manager():
    return RelationshipManager()

@pytest.fixture
def people():
    return [
        Person(name="Alice"),
        Person(name="Bob"),
        Person(name="Claire")
    ]

def test_set_and_get_relationship(relationship_manager, people):
    p1, p2 = people[0], people[1]
    relationship_manager.set_relationship(p1, p2, trust=80, resentment=10)
    rel = relationship_manager.get_relationship(p1, p2)
    assert rel is not None
    assert rel.trust == 80
    assert rel.resentment == 10

def test_update_existing_relationship(relationship_manager, people):
    p1, p2 = people[0], people[1]
    relationship_manager.set_relationship(p1, p2, trust=60, resentment=5)
    relationship_manager.update_relationship(p1, p2, trust=70)
    rel = relationship_manager.get_relationship(p1, p2)
    assert rel.trust == 70
    assert rel.resentment == 5

def test_update_nonexistent_relationship(relationship_manager, people):
    p1, p2 = people[0], people[1]
    relationship_manager.update_relationship(p1, p2, trust=90, resentment=20)
    rel = relationship_manager.get_relationship(p1, p2)
    assert rel is not None
    assert rel.trust == 90
    assert rel.resentment == 20

def test_get_outgoing_relationships(relationship_manager, people):
    p1, p2, p3 = people
    relationship_manager.set_relationship(p1, p2, trust=55)
    relationship_manager.set_relationship(p1, p3, trust=45)
    relationship_manager.set_relationship(p2, p1, trust=20)

    outgoing = relationship_manager.get_outgoing_relationships(p1)
    assert len(outgoing) == 2
    assert p2.id in outgoing
    assert p3.id in outgoing
    assert p1.id not in outgoing

def test_init_all_relationships(relationship_manager, people):
    relationship_manager.init_all_relationships(people, trust=60, resentment=15)
    assert len(relationship_manager.relations) == 6
    assert relationship_manager.get_relationship(people[0], people[1]) is not None
    assert relationship_manager.get_relationship(people[1], people[0]) is not None
    assert relationship_manager.get_relationship(people[0], people[1]).trust == 60
    assert relationship_manager.get_relationship(people[0], people[1]).resentment == 15

def test_init_all_relationships_with_randomization(relationship_manager, people):
    trust_base = 70
    resentment_base = 10
    radius = 10
    relationship_manager.init_all_relationships(people, trust=trust_base, resentment=resentment_base, randomize_range=radius)

    for rel in relationship_manager.relations.values():
        assert trust_base - radius <= rel.trust <= trust_base + radius
        assert resentment_base - radius <= rel.resentment <= resentment_base + radius

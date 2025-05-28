import pytest
import random
from simulation.simclass import Simulation
from simulation.person import Person
from simulation.relationships import Relationship
from simulation.npcconvo import NPCConvo
from simulation.settings import *

# Mock random for deterministic testing
@pytest.fixture(autouse=True)
def mock_random(monkeypatch):
    def mock_randint(a, b):
        return a
    def mock_random():
        return 0.5
    def mock_choice(seq):
        return seq[0]
    monkeypatch.setattr(random, 'randint', mock_randint)
    monkeypatch.setattr(random, 'random', mock_random)
    monkeypatch.setattr(random, 'choice', mock_choice)

# Basic initialization tests
def test_simulation_initialization():
    sim = Simulation()
    assert isinstance(sim.id, str)
    assert sim.people == {}
    assert sim.relationships == {}
    assert sim.tick_count == 0
    assert sim.conversations == {}
    assert sim.rumors == {}
    assert sim.min_convos == 0
    assert sim.max_convos == 3

def test_simulation_initialization_with_id():
    custom_id = "test123"
    sim = Simulation(id=custom_id)
    assert sim.id == custom_id
    assert sim.people == {}
    assert sim.conversations == {}

def test_simulation_initialization_with_people():
    people = [Person(name="John"), Person(name="Jane")]
    sim = Simulation(people=people)
    assert len(sim.people) == 2
    assert sim.people[people[0].id].name == "John"
    assert sim.people[people[1].id].name == "Jane"
    assert len(sim.relationships) == 1

    min_id = min(people[0].id, people[1].id)
    max_id = max(people[0].id, people[1].id)
    rkey = (min_id, max_id)
    assert sim.relationships[rkey].person1.id == min_id
    assert sim.relationships[rkey].person2.id == max_id

def test_simulation_from_json():
    sim = Simulation(from_json="simulation-test-simulation.json")
    assert sim.id == "test-sim-123"
    assert len(sim.people) == 2
    assert sim.people["test-person-1"].id == "test-person-1"
    assert sim.people["test-person-2"].id == "test-person-2"

    rel = sim.relationships[("test-person-1", "test-person-2")]
    assert rel.trust == 222
    assert rel.animosity == 333

def test_simulation_bad_json():
    with pytest.raises(FileNotFoundError):
        sim = Simulation(from_json="nonexistent.json")

# Relationship management tests
def test_initialize_missing_relationships():
    people = [Person(name="John"), Person(name="Jane"), Person(name="Bob")]
    sim = Simulation(people=people)
    assert len(sim.relationships) == 3  # Should have relationships between all pairs

def test_get_relationship():
    p1 = Person(name="John")
    p2 = Person(name="Jane")
    sim = Simulation(people=[p1, p2])
    rel = sim.get_relationship(p1, p2)
    assert isinstance(rel, Relationship)
    assert rel.person1 in [p1, p2]
    assert rel.person2 in [p1, p2]

# Conversation management tests
def test_initialize_conversations():
    people = [Person(name="John"), Person(name="Jane"), Person(name="Bob")]
    sim = Simulation(people=people, min_convos=1, max_convos=2)
    assert len(sim.conversations) >= sim.min_convos
    assert len(sim.conversations) <= sim.max_convos

def test_lucky_begin_conversation():
    people = [Person(name="John"), Person(name="Jane"), Person(name="Bob")]
    sim = Simulation(people=people, min_convos=0, max_convos=3)
    initial_convo_count = len(sim.conversations)
    sim.lucky_begin_conversation()
    assert len(sim.conversations) >= initial_convo_count

def test_lucky_end_conversation():
    people = [Person(name="John"), Person(name="Jane"), Person(name="Bob")]
    sim = Simulation(people=people, min_convos=0, max_convos=3)
    sim.initialize_conversations()
    initial_convo_count = len(sim.conversations)
    sim.lucky_end_conversation()
    assert len(sim.conversations) <= initial_convo_count

def test_lucky_manage_people_in_conversations():
    people = [Person(name="John"), Person(name="Jane"), Person(name="Bob")]
    sim = Simulation(people=people, min_convos=1, max_convos=2)
    sim.initialize_conversations()
    initial_convo_count = len(sim.conversations)
    sim.lucky_manage_people_in_conversations()
    assert len(sim.conversations) == initial_convo_count

# Fight detection tests
def test_check_for_fight():
    p1 = Person(name="John")
    p2 = Person(name="Jane")
    sim = Simulation(people=[p1, p2])
    rel = sim.get_relationship(p1, p2)
    
    # Set conditions for a fight
    p1.anger = MIN_ANGER_FOR_FIGHT + 1
    p2.anger = MIN_ANGER_FOR_FIGHT + 1
    rel.animosity = MIN_ANIMOSITY_FOR_FIGHT + 1
    
    assert sim.check_for_fight(rel) is True

def test_check_for_fight_no_fight():
    p1 = Person(name="John")
    p2 = Person(name="Jane")
    sim = Simulation(people=[p1, p2])
    rel = sim.get_relationship(p1, p2)
    
    # Set conditions below fight thresholds
    p1.anger = MIN_ANGER_FOR_FIGHT - 1
    p2.anger = MIN_ANGER_FOR_FIGHT - 1
    rel.animosity = MIN_ANIMOSITY_FOR_FIGHT - 1
    
    assert sim.check_for_fight(rel) is False

# Tick functionality tests
def test_tick_anger_reduction():
    p1 = Person(name="John")
    p2 = Person(name="Jane")
    sim = Simulation(people=[p1, p2])
    
    p1.anger = 100
    p2.anger = 100
    initial_anger1 = p1.anger
    initial_anger2 = p2.anger
    
    sim.tick()
    
    assert p1.anger == initial_anger1 - ANGER_DROP_PER_TICK
    assert p2.anger == initial_anger2 - ANGER_DROP_PER_TICK
    assert sim.tick_count == 1

def test_tick_conversation_progression():
    people = [Person(name="John"), Person(name="Jane")]
    sim = Simulation(people=people, min_convos=1, max_convos=1)
    sim.initialize_conversations()
    
    initial_tick_count = next(iter(sim.conversations.values())).tick_count
    sim.tick()
    new_tick_count = next(iter(sim.conversations.values())).tick_count
    
    assert new_tick_count == initial_tick_count + 1

# Edge cases and error conditions
def test_initialize_conversations_no_people():
    sim = Simulation(people=[])
    sim.initialize_conversations()
    assert len(sim.conversations) == 0

def test_get_relationship_same_person():
    p1 = Person(name="John")
    sim = Simulation(people=[p1])
    with pytest.raises(KeyError):
        sim.get_relationship(p1, p1)

def test_initialize_conversations_max_participants():
    people = [Person(name=f"Person{i}") for i in range(10)]
    sim = Simulation(people=people, min_convos=1, max_convos=1)
    # Don't call initialize_conversations() again since it's called in __init__
    assert len(sim.conversations) >= sim.min_convos
    assert len(sim.conversations) <= sim.max_convos
    if sim.conversations:
        convo = next(iter(sim.conversations.values()))
        assert len(convo.participants) <= len(people) // sim.max_convos + 1

def test_initialize_conversations_direct():
    """Test initialize_conversations() directly on a simulation without initial conversations"""
    people = [Person(name=f"Person{i}") for i in range(10)]
    sim = Simulation(people=people, min_convos=0, max_convos=0)  # Set to 0 to prevent init from creating conversations
    sim.initialize_conversations()
    assert len(sim.conversations) >= sim.min_convos
    assert len(sim.conversations) <= sim.max_convos
    if sim.conversations:
        convo = next(iter(sim.conversations.values()))
        assert len(convo.participants) <= len(people) // sim.max_convos + 1
import pytest
from simulation.person import Person, RANDOM_NAMES, MBTI
import random
import os

def test_person_initialization_with_name():
    person = Person(name="John")
    assert person.name == "John"
    assert person.is_npc is True
    assert person.secrets == []
    assert person.rumors == set()
    assert isinstance(person.anger, (int, float))
    assert isinstance(person.gullibility, (int, float))
    assert isinstance(person.convo_stay, (int, float))

def test_person_initialization_without_name():
    person = Person()
    assert person.name in RANDOM_NAMES
    assert person.is_npc is True

def test_person_initialization_with_custom_id():
    custom_id = "test123"
    person = Person(id=custom_id)
    assert person.id == custom_id

def test_person_initialization_with_secrets_and_rumors():
    secrets = ["secret1", "secret2"]
    rumors = ["rumor1", "rumor2"]
    person = Person(secrets=secrets, rumors=rumors)
    assert person.secrets == secrets
    assert person.rumors == set(rumors)

def test_person_initialization_with_stats():
    anger = 100
    gullibility = 200
    convo_stay = 300
    gossip_level = 400
    person = Person(anger=anger, gullibility=gullibility, convo_stay=convo_stay, gossip_level=gossip_level)
    assert person.anger == anger
    assert person.gullibility == gullibility
    assert person.convo_stay == convo_stay
    assert person.gossip_level == gossip_level

def test_person_initialization_with_randomize_stats():
    base_anger = 100
    base_gossip = 500
    randomize_stats = 50
    person = Person(anger=base_anger, gossip_level=base_gossip, randomize_stats=randomize_stats)
    # The actual value will be within base_anger ± randomize_stats
    assert base_anger - randomize_stats <= person.anger <= base_anger + randomize_stats
    assert base_gossip - randomize_stats <= person.gossip_level <= base_gossip + randomize_stats

def test_person_from_json():
    person = Person(from_json="person-test-person-1.json")
    assert person.id == "test-person-1"
    assert person.name == "Test Person"
    assert person.mbti == "INTJ"
    assert person.description == "A test person for unit testing"
    assert person.is_npc is True
    assert person.anger == 100
    assert person.gullibility == 500
    assert person.convo_stay == 500
    assert person.gossip_level == 500
    assert len(person.secrets) == 1
    assert person.secrets[0].id == 'test-secret-1'
    assert person.rumors == set()

def test_person_pretty_print(capsys):
    person = Person(name="TestPerson", id="test123")
    person.pretty_print()
    captured = capsys.readouterr()
    assert "Person:" in captured.out
    assert "ID: test123" in captured.out
    assert "Name: TestPerson" in captured.out
    assert "NPC: True" in captured.out

def test_person_mbti_initialization():
    # Test custom MBTI
    person = Person(mbti="INTJ")
    assert person.mbti == "INTJ"
    
    # Test random MBTI
    person = Person()
    assert person.mbti in MBTI

def test_person_description():
    description = "A mysterious person who loves to dance"
    person = Person(description=description)
    assert person.description == description
    
    # Test empty description
    person = Person()
    assert person.description == ""

def test_person_conversation_methods():
    person = Person()
    mock_convo = "mock_conversation"  # In real usage this would be an NPCConvo instance
    
    # Test adding to conversation
    person.add_to_convo(mock_convo)
    assert person.active_conversation == mock_convo
    assert person.active_conversation_ticks == 0
    assert person.active_conversation_max_ticks > 0
    
    # Test removing from conversation
    person.remove_from_convo()
    assert person.active_conversation is None
    assert person.active_conversation_ticks == 0
    assert person.active_conversation_max_ticks == 0

def test_person_reduce_anger():
    person = Person(anger=100)
    
    # Test normal reduction
    person.modify_anger(-30)
    assert person.anger == 70
    
    # Test reduction below zero
    person.modify_anger(-100)
    assert person.anger == 0

def test_person_pretty_print_comprehensive(capsys):
    person = Person(
        name="TestPerson",
        id="test123",
        mbti="INTJ",
        description="A test description",
        is_npc=False,
        anger=100,
        gullibility=200,
        convo_stay=300,
        gossip_level=400
    )

    class Filler:
        def __init__(self, id):
            self.id = id

    # Add some secrets and rumors
    person.secrets = [Filler("secret1"), Filler("secret2")]
    person.rumors = [Filler("rumor1"), Filler("rumor2")]
    
    person.pretty_print()
    captured = capsys.readouterr()
    output = captured.out
    
    # Test all fields are present in output
    assert "Person:" in output
    assert "ID: test123" in output
    assert "Name: TestPerson" in output
    assert "NPC: False" in output
    assert "MBTI: INTJ" in output
    assert "Description: A test description" in output
    assert "Anger: 100" in output
    assert "Gullibility: 200" in output
    assert "Convo Stay: 300" in output
    assert "Gossip Level: 400" in output
    assert "Secrets IDs: ['secret1', 'secret2']" in output
    assert "Rumors IDs: ['rumor1', 'rumor2']" in output

def test_person_random_name_selection():
    # Test multiple random name selections
    names = set()
    for _ in range(100):  # Generate 100 random names
        person = Person()
        names.add(person.name)
    
    # Verify that we get different names and they're all valid
    assert len(names) > 1  # Should get at least 2 different names
    assert all(name in RANDOM_NAMES for name in names)

def test_person_is_npc_flag():
    # Test NPC flag
    person = Person(is_npc=True)
    assert person.is_npc is True
    
    # Test non-NPC flag
    person = Person(is_npc=False)
    assert person.is_npc is False
    
    # Test default value
    person = Person()
    assert person.is_npc is True 

def test_person_modify_anger_with_floor_ceiling():
    # Test normal reduction
    person = Person(anger=100)
    person.modify_anger(-30)
    assert person.anger == 70
    
    # Test reduction below zero (should floor at 0)
    person = Person(anger=50)
    person.modify_anger(-100)
    assert person.anger == 0
    
    # Test reduction with decimal values (should round)
    person = Person(anger=100)
    person.modify_anger(30.7)
    assert person.anger == 131  # 100 + 30.7 = 130.7, should round to 131
    
    # Test reduction with very small values
    person = Person(anger=100)
    person.modify_anger(0.1)
    assert person.anger == 100  # Should round to 100
    
    # Test reduction with very large values
    person = Person(anger=100)
    person.modify_anger(-1000)
    assert person.anger == 0  # Should floor at 0


    # Test reduction with very large values
    person = Person(anger=100)
    person.modify_anger(1000)
    assert person.anger == 1000  # Should floor at 1000
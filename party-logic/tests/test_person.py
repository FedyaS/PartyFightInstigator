import pytest
from simulation.person import Person, RANDOM_NAMES
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
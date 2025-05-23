import pytest
from simulation.person import Person, RANDOM_NAMES
import random

def test_person_initialization_with_name():
    person = Person(name="John")
    assert person.name == "John"
    assert person.is_npc is True
    assert person.secret_ids == []
    assert person.rumor_ids == []
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
    assert person.secret_ids == secrets
    assert person.rumor_ids == rumors

def test_person_initialization_with_stats():
    anger = 100
    gullibility = 200
    convo_stay = 300
    person = Person(anger=anger, gullibility=gullibility, convo_stay=convo_stay)
    assert person.anger == anger
    assert person.gullibility == gullibility
    assert person.convo_stay == convo_stay

def test_person_initialization_with_randomize_stats():
    base_anger = 100
    randomize_stats = 50
    person = Person(anger=base_anger, randomize_stats=randomize_stats)
    # The actual value will be within base_anger ± randomize_stats
    assert base_anger - randomize_stats <= person.anger <= base_anger + randomize_stats

def test_person_pretty_print(capsys):
    person = Person(name="TestPerson", id="test123")
    person.pretty_print()
    captured = capsys.readouterr()
    expected_output = (
        "Person: (ID: test123)\n"
        "    Name: TestPerson\n"
        "    NPC: True\n"
        "    Secrets: []\n"
        "    Rumors: []\n"
        "    Anger: 0\n"
        "    Gullibility: 500\n"
        "    Convo_Stay: 500\n"
    )
    assert captured.out == expected_output 
import pytest
from simulation.simclass import Simulation
from simulation.person import Person

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
import pytest
from simulation.simclass import Simulation
from simulation.person import Person

def test_simulation_initialization():
    sim = Simulation()
    assert isinstance(sim.id, str)
    assert sim.people == []

def test_simulation_initialization_with_id():
    custom_id = "test123"
    sim = Simulation(id=custom_id)
    assert sim.id == custom_id
    assert sim.people == []

def test_simulation_initialization_with_people():
    people = [Person(name="John"), Person(name="Jane")]
    sim = Simulation(people=people)
    assert len(sim.people) == 2
    assert sim.people[0].name == "John"
    assert sim.people[1].name == "Jane"

def test_simulation_from_json():
    sim = Simulation(from_json="simulation-test-simulation.json")
    assert sim.id == "test-sim-123"
    assert len(sim.people) == 2
    assert sim.people[0].id == "test-person-1"
    assert sim.people[1].id == "test-person-2"

def test_simulation_empty_json():
    sim = Simulation(from_json="nonexistent.json")
    assert isinstance(sim.id, str)
    assert sim.people == [] 
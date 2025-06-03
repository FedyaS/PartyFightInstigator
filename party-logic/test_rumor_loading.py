#!/usr/bin/env python3

from simulation.rumor import Rumor
from simulation.person import Person

def test_rumor_loading():
    print("Testing rumor loading...")
    
    # Test loading a rumor from JSON with a mock subject
    try:
        class MockPerson:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        
        mock_subject = MockPerson("Nicholas", "Nicholas Gente")
        rumor = Rumor(from_json="rumor-Nicholas1.json", subjects=[mock_subject])
        print(f"Successfully loaded rumor: {rumor.id}")
        print(f"Text: {rumor.text}")
        print(f"Is really true: {rumor.is_really_true}")
        print(f"Subjects: {[s.name for s in rumor.subjects]}")
        print(f"Originators: {rumor.originators}")
        print(f"Self conceal score: {rumor.self_conceal_score}")
    except Exception as e:
        print(f"Error loading rumor: {e}")
    
    # Test loading a person with rumors
    try:
        person = Person(from_json="person-Nicholas.json")
        print(f"\nSuccessfully loaded person: {person.name}")
        print(f"Person ID: {person.id}")
        print(f"Number of rumors: {len(person.rumors)}")
        for rumor in person.rumors:
            print(f"  - Rumor ID: {rumor.id}")
            print(f"    Subjects: {[s.name for s in rumor.subjects]}")
            print(f"    Originators: {rumor.originators}")
    except Exception as e:
        print(f"Error loading person with rumors: {e}")

if __name__ == "__main__":
    test_rumor_loading() 
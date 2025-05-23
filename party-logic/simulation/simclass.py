import os
import json

from simulation.utils import create_id, load_json

from simulation.person import Person
from simulation.npcsecret import NPCSecret
from simulation.rumor import Rumor

class Simulation:
    def __init__(self, id=None, people=None, from_json=''):
        data = load_json(from_json)
        if data:
            self.id = data['id']
            self.people = [Person(from_json=f"person-{pid}.json") for pid in data['person_ids']]

        else:
            if people is None:
                people = []
            self.id = id or create_id()
            self.people = people

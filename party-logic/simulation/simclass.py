import os
import json

from utils import create_id, load_json

from person import Person
from secret import Secret
from rumor import Rumor

class Simulation:
    def __init__(self, id=None, from_json=''):
        data = load_json(from_json)
        if data:
            self.id = data['id']
            self.people = [Person(from_json=f"person-{pid}.json") for pid in data['person_ids']]

        else:
            self.id = id or create_id()
            self.people = []

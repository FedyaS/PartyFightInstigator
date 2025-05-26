import os
import json
from typing import List

from simulation.utils import create_id, load_json

from simulation.person import Person
from simulation.npcsecret import NPCSecret
from simulation.rumor import Rumor

from simulation.settings import *

class Simulation:
    def __init__(self, id=None, people: List[Person] = None, from_json=''):
        data = load_json(from_json, 'simulation')
        if data:
            self.id = data['id']
            self.people = [Person(from_json=f"person-{pid}.json") for pid in data['person_ids']]
            self.people = {pid: Person(from_json=f"person-{pid}.json") for pid in data['person_ids']}

        else:
            if people is None:
                people = {}
            self.id = id or create_id()
            self.people = {p.id: p for p in people}

        self.tick_count = 0
        self.conversations = {}
        self.rumors = {}
        self.relationships = {}


    def tick(self):
        for p in self.people:
            p.reduce_anger(ANGER_DROP_PER_TICK)




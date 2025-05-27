import os
import json
import random
from typing import List

from simulation.utils import create_id, load_json, get_cross_id

from simulation.person import Person
from simulation.relationships import Relationship
from simulation.npcconvo import NPCConvo
from simulation.npcsecret import NPCSecret
from simulation.rumor import Rumor

from simulation.settings import *

class Simulation:
    def __init__(self, id=None, people: List[Person] = None, min_convos: int = 0, max_convos: int = 3, from_json=''):
        data = load_json(from_json, 'simulation')
        if data:
            self.id = data['id']
            self.min_convos = data['min_convos']
            self.max_convos = data['max_convos']
            self.people = {pid: Person(from_json=f"person-{pid}.json") for pid in data['person_ids']}
            self.relationships = {}
            for r in data['relationships']:
                p1 = self.people[r['person1_id']]
                p2 = self.people[r['person2_id']]
                new_rel = Relationship(p1, p2, r['trust'], r['animosity'])
                self.relationships[new_rel.id] = new_rel
        else:
            if people is None:
                people = {}
            self.id = id or create_id()
            self.min_convos = min_convos
            self.max_convos = max_convos
            self.people = {p.id: p for p in people}
            self.relationships = {}

        # Check that all relationships are created, and create any missing ones
        self.initialize_missing_relationships()

        self.tick_count = 0
        self.conversations = {}
        self.initialize_conversations()
        self.rumors = {}

    def initialize_missing_relationships(self):
        for p1 in self.people.values():
            for p2 in self.people.values():
                if p1.id != p2.id:
                    if get_cross_id(p1.id, p2.id) not in self.relationships:
                        new_rel = Relationship(p1, p2, randomize_stats=200)
                        self.relationships[new_rel.id] = new_rel

    def initialize_conversations(self):
        initial_convos = random.randint(self.min_convos, self.max_convos)
        min_participants = 1
        max_participants = len(self.people) // self.max_convos + 1
        available_people = list(self.people.values())
        available_people = [p for p in available_people if p.active_conversation is None]

        for _ in range(initial_convos):
            if not available_people:
                break

            num_participants = random.randint(min_participants, max_participants)
            participants = random.sample(available_people, num_participants)

            if len(participants) >= min_participants:
                conv = NPCConvo(participants)
                self.conversations[conv.id] = conv
                available_people = [p for p in available_people if p.active_conversation is None]

    def lucky_end_conversation(self):
        # End a Convo
        chance_will_end = CHANCE_TO_END_CONVO_PER_TICK / MAX_VAL
        if (
                len(self.conversations) > self.min_convos and
                random.random() < chance_will_end
        ):
            conv_to_end: NPCConvo = random.choice(list(self.conversations.values()))
            conv_to_end.end_conversation()
            self.conversations.pop(conv_to_end.id)


    def lucky_begin_conversation(self):
        # Start a Convo
        chance_will_start = CHANCE_TO_START_CONVO_PER_TICK / MAX_VAL
        if (
                len(self.conversations) < self.max_convos and
                random.random() > chance_will_start
        ):

            available_people = list(self.people.values())
            available_people = [p for p in available_people if p.active_conversation is None]
            min_participants = 1
            max_participants = len(available_people) // self.max_convos + 1
            num_participants = random.randint(min_participants, max_participants)
            participants = random.sample(available_people, num_participants)

            if len(participants) >= min_participants:
                conv = NPCConvo(participants)
                self.conversations[conv.id] = conv


    def tick(self):
        for p in self.people.values():
            p.reduce_anger(ANGER_DROP_PER_TICK)

        for c in self.conversations.values():
            c.tick()

        for r in self.relationships.values():
            if r.animosity > 10000:
                # start fight
                pass

        self.lucky_begin_conversation()
        self.lucky_end_conversation()
        # Manage creation and deletion of conversations
        # Manage people going into and out of conversations

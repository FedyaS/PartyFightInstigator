from typing import List

from simulation.utils import create_id, apply_random_modifier
from simulation.person import Person

class NPCConvo:
    def __init__(self, participants: List[Person], id: str=None, max_tick_count=1000, randomize_stats=0):
        self.id = id or create_id()
        self.participants = participants
        self.max_tick_count = apply_random_modifier(max_tick_count, randomize_stats)
        self.tick_count = 0

        for person in participants:
            if person.active_conversation is not None:
                raise ValueError(f"Person {person.id} is already in a conversation")

            person.active_conversation = self

    def add_person(self, person: Person):
        if person.active_conversation is not None:
            raise ValueError(f"Person {person.id} is already in a conversation")

        self.participants.append(person)
        person.active_conversation = self

    def remove_person(self, person: Person):
        if person not in self.participants:
            raise ValueError(f"Person {person.id} is not in this conversation")

        self.participants.remove(person)
        person.active_conversation = None

    def end_conversation(self):
        for person in self.participants:
            person.active_conversation = None
        self.participants = []
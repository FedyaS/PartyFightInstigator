from typing import List

from simulation.utils import create_id
from simulation.person import Person

class NPCConvo:
    def __init__(self, participants: List[Person], id: str=None, max_tick_count=1000):
        self.id = id or create_id()
        self.participants = participants
        self.max_tick_count = max_tick_count
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
        self.participants.remove(person)
        person.active_conversation = None
import random
from simulation.utils import create_id, apply_random_modifier

RANDOM_NAMES = ['Tom', 'Bob', 'Joe', 'Henry', 'Will', 'Kevin', 'Alice', 'Dasha', 'Olivia', 'Janet', 'Claire']

class Person:
    def __init__(self, name=None, id=None, is_npc=True,
                 anger=0, gullibility=500, convo_stay=500, randomize_stats=0,
                 secrets=None, rumors=None):

        if secrets is None:
            secrets = []
        if rumors is None:
            rumors = []

        self.name = name or random.choice(RANDOM_NAMES)
        self.id = id or create_id()
        self.is_npc = is_npc
        self.secret_ids = secrets
        self.rumor_ids = rumors

        self.anger = apply_random_modifier(anger, randomize_stats)
        self.gullibility = apply_random_modifier(gullibility, randomize_stats)
        self.convo_stay = apply_random_modifier(convo_stay, randomize_stats)
    
    def pretty_print(self):
        print(f"Person: (ID: {self.id})")
        print(f"    Name: {self.name}")
        print(f"    NPC: {self.is_npc}")
        print(f"    Secrets: {self.secret_ids}")
        print(f"    Rumors: {self.rumor_ids}")
        print(f"    Anger: {self.anger}")
        print(f"    Gullibility: {self.gullibility}")
        print(f"    Convo_Stay: {self.convo_stay}")
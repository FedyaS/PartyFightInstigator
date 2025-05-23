import random
from simulation.emotional_state import EmotionalState
from simulation.utils import create_id

RANDOM_NAMES = ['Tom', 'Bob', 'Joe', 'Henry', 'Will', 'Kevin', 'Alice', 'Dasha', 'Olivia', 'Janet', 'Claire']

class Person:
    def __init__(self, name=None, id=None, is_npc=True, randomize_emotions=0):
        self.name = name or random.choice(RANDOM_NAMES)
        self.id = id or create_id()
        self.is_npc = is_npc
        self.rumor_ids = []

        # Emotional State
        self.ES = EmotionalState(randomize_radius=randomize_emotions)
    
    def pretty_print(self):
        print(f"Person: {self.name} (ID: {self.id})")
        print(f"  NPC: {self.is_npc}")
        print(f"  Rumors: {self.rumor_ids}")
        print("  Emotional State:")
        print(f"    Joy:       {self.ES.joy}")
        print(f"    Anger:     {self.ES.anger}")
        print(f"    Anxiety:   {self.ES.anxiety}")
        print(f"    Jealousy:  {self.ES.jealousy}")
        print(f"    Curiosity: {self.ES.curiosity}")

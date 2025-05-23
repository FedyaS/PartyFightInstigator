import random
from simulation.utils import apply_random_modifier

class EmotionalState:
    def __init__(self, joy=50, anger=10, anxiety=50, jealousy=10, curiosity=50, randomize_radius=0):
        self.joy = apply_random_modifier(joy, randomize_radius) if randomize_radius else joy
        self.anger = apply_random_modifier(anger, randomize_radius) if randomize_radius else anger
        self.anxiety = apply_random_modifier(anxiety, randomize_radius) if randomize_radius else anxiety
        self.jealousy = apply_random_modifier(jealousy, randomize_radius) if randomize_radius else jealousy
        self.curiosity = apply_random_modifier(curiosity, randomize_radius) if randomize_radius else curiosity
    
    def set_emotional_state(self, **kwargs):
        for emotion in ['joy', 'anger', 'anxiety', 'jealousy', 'curiosity']:
            if emotion in kwargs:
                setattr(self, emotion, kwargs[emotion])
    
    def pretty_print(self):
        print("Emotional State:")
        print(f"  Joy:       {self.joy}")
        print(f"  Anger:     {self.anger}")
        print(f"  Anxiety:   {self.anxiety}")
        print(f"  Jealousy:  {self.jealousy}")
        print(f"  Curiosity: {self.curiosity}")

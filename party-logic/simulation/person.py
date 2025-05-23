import random
from simulation.utils import create_id, apply_random_modifier, load_json

from npcsecret import NPCSecret

RANDOM_NAMES = ['Tom', 'Bob', 'Joe', 'Henry', 'Will', 'Kevin', 'Alice', 'Dasha', 'Olivia', 'Janet', 'Claire']
MBTI = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

class Person:
    def __init__(self, id=None, name=None, mbti=None, description='', is_npc=True,
                 anger=0, gullibility=500, convo_stay=500, randomize_stats=0,
                 secrets=None, rumor_ids=None, from_json=''):
        data = load_json(from_json)
        if data:
            self.id = data['id']
            self.name = data['name']
            self.mbti = data['mbti']
            self.description = data['description']
            self.is_npc = data['is_npc']

            self.anger = data['anger']
            self.gullibility = data['gullibility']
            self.convo_stay = data['convo_stay']

            self.secrets = [NPCSecret(from_json=f"secret-{sid}.json") for sid in data['secret_ids']]
            self.rumor_ids = data['rumor_ids']

        else:
            if secrets is None:
                secrets = []
            if rumor_ids is None:
                rumor_ids = []

            self.id = id or create_id()
            self.name = name or random.choice(RANDOM_NAMES)
            self.mbti = mbti or random.choice(MBTI)
            self.description = description
            self.is_npc = is_npc

            self.anger = apply_random_modifier(anger, randomize_stats)
            self.gullibility = apply_random_modifier(gullibility, randomize_stats)
            self.convo_stay = apply_random_modifier(convo_stay, randomize_stats)

            self.secrets = secrets
            self.rumor_ids = rumor_ids

    def pretty_print(self, indent=4):
        attrs = {
            "ID": self.id,
            "Name": self.name,
            "NPC": self.is_npc,
            "MBTI": self.mbti,
            "Description": self.description,
            "Anger": self.anger,
            "Gullibility": self.gullibility,
            "Convo Stay": self.convo_stay,
            "Secrets": [s.id for s in self.secrets] if self.secrets else "None",
            "Rumor IDs": self.rumor_ids if self.rumor_ids else "None"
        }
        print("Person:")
        for key, value in attrs.items():
            print(f"{' ' * indent}{key}: {value}")
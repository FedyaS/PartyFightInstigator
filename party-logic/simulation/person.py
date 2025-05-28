import random
from typing import TYPE_CHECKING, Set, List

from simulation.rumor import Rumor
from simulation.utils import create_id, apply_random_modifier, load_json, floor_ceiling_round
from simulation.npcsecret import NPCSecret

if TYPE_CHECKING:
    from simulation.npcconvo import NPCConvo

RANDOM_NAMES = ['Tom', 'Bob', 'Joe', 'Henry', 'Will', 'Kevin', 'Alice', 'Dasha', 'Olivia', 'Janet', 'Claire']
MBTI = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

class Person:
    def __init__(self, id=None, name=None, mbti=None, description='', is_npc=True,
                 anger=0, gullibility=500, convo_stay=500, gossip_level=500, randomize_stats=0,
                 secrets=None, rumors=None, from_json=''):
        data = load_json(from_json, 'person')
        if data:
            self.id = data['id']
            self.name = data['name']
            self.mbti = data['mbti']
            self.description = data['description']
            self.is_npc = data['is_npc']

            self.anger = data['anger']
            self.gullibility = data['gullibility']
            self.convo_stay = data['convo_stay']
            self.gossip_level = data['gossip_level']

            self.secrets = [NPCSecret(from_json=f"npcsecret-{sid}.json") for sid in data['secret_ids']]
            self.rumors = set() # No loading rumors from json for now

        else:
            if secrets is None:
                secrets = []
            self.secrets = secrets

            if rumors is None:
                rumors = []
            self.rumors = set(rumors)

            self.id = id or create_id()
            self.name = name or random.choice(RANDOM_NAMES)
            self.mbti = mbti or random.choice(MBTI)
            self.description = description
            self.is_npc = is_npc

            self.anger = apply_random_modifier(anger, randomize_stats)
            self.gullibility = apply_random_modifier(gullibility, randomize_stats)
            self.convo_stay = apply_random_modifier(convo_stay, randomize_stats)
            self.gossip_level = apply_random_modifier(gossip_level, randomize_stats)

        self.active_conversation: 'NPCConvo' = None
        self.active_conversation_ticks = 0
        self.active_conversation_max_ticks = 0

    def add_to_convo(self, conversation: 'NPCConvo'):
        self.active_conversation = conversation
        self.active_conversation_ticks = 0
        will_stay_for = apply_random_modifier(self.convo_stay, 200)
        self.active_conversation_max_ticks = will_stay_for

    def remove_from_convo(self):
        self.active_conversation = None
        self.active_conversation_ticks = 0
        self.active_conversation_max_ticks = 0

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
            "Gossip Level": self.gossip_level,
            "Secrets IDs": [s.id for s in self.secrets] if self.secrets else "None",
            "Rumors IDs": [r.id for r in self.rumors] if self.rumors else "None"
        }
        print("Person:")
        for key, value in attrs.items():
            print(f"{' ' * indent}{key}: {value}")

    def reduce_anger(self, a):
        self.anger = floor_ceiling_round(self.anger - a)
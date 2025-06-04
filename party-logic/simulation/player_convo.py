from typing import TYPE_CHECKING

import random

from simulation.relationships import Relationship
from simulation.utils import floor_ceiling_round
from simulation.llm_prompt import construct_prompt
from simulation.llm_handler import get_llm_response
from simulation.llm_helper import *
from simulation.settings import *
from simulation.rumor import Rumor

if TYPE_CHECKING:
    from simulation.person import Person
    from simulation.simclass import Simulation

class PlayerConvo:
    def __init__(self, npc: 'Person', trust=500, animosity=500):
        self.npc = npc
        self.trust = trust
        self.animosity = animosity
        self.conversation = []

    def change_trust(self, amount):
        self.trust = floor_ceiling_round(self.trust + amount)

    def change_animosity(self, amount):
        self.animosity = floor_ceiling_round(self.animosity + amount)

    def hear_new_rumor(self, nri: NewRumorIntent, simulation: 'Simulation'):
        if nri.id_existing_rumor:
            return

        subjects = []
        for s in nri.subjects:
            person = simulation.safe_get_person(s.id)
            if person:
                subjects.append(person)
        originators = []
        for o in nri.originators:
            person = simulation.safe_get_person(o.id)
            if person:
                originators.append(person)

        rumor = Rumor(text=nri.text, hash_text=nri.hash_text,
                      plausibility=nri.plausibility, harmfulness=nri.harmfulness,
                      subjects=subjects, originators=originators)

        believed_chance = RUMOR_BELIEVABILITY * (
                self.npc.gullibility / MAX_VAL *
                self.trust / MAX_VAL *
                rumor.plausibility / MAX_VAL)
        believed_it = random.random() < believed_chance
        rumor_is_about_this_person = self.npc in rumor.subjects

        if rumor_is_about_this_person:
            self.npc.modify_anger(rumor.harmfulness)
            # self.change_animosity(rumor.harmfulness)
            # self.change_trust(-rumor.harmfulness / 2)
            for originator in rumor.originators:
                rel = simulation.get_relationship(self.npc, originator)
                rel.modify_animosity(rumor.harmfulness)
                rel.modify_trust(-rumor.harmfulness / 2)

        elif believed_it:
            self.change_trust(TRUST_INCREASE_ON_RUMOR_BELIEF)
            self.npc.modify_anger(rumor.harmfulness * ANGER_INCREASE_PER_RUMOR_HARM)
            self.npc.rumors.add(rumor)

            # Animosity towards subjects growths if the rumor was harmful
            if (
                    self.npc not in rumor.subjects and
                    rumor.harmfulness > MIN_RUMOR_HARMFULNESS_TO_GROW_ANIMOSITY
            ):
                for subject in rumor.subjects:
                    rel = simulation.get_relationship(self.npc, subject)
                    rel.modify_animosity(rumor.harmfulness)
                    rel.modify_trust(-rumor.harmfulness / 2)

        elif not believed_it:
            self.change_trust(-TRUST_DECREASE_ON_RUMOR_DISBELIEF)

    def talk(self, player_text: str, simulation: 'Simulation'):
        relationships = simulation.get_all_relationships_for_person(self.npc)
        prompt = construct_prompt(player_text, self.npc, relationships, self.npc.rumors, self.trust, self.animosity)
        response = get_llm_response(prompt)

        if not response:
            print("Failed LLM Call")
        elif response.out_of_scope:
            print("Out of Scope")
        elif response.chat_intent:
            print("Chat Intent")
            return response.npc_response_to_player
        elif response.learn_intent:
            print("Learn Intent")
            return response.npc_response_to_player
        elif response.influence_intent:
            print("Influence Intent")
            for influence in response.influence_intent.influences:
                other_person = simulation.safe_get_person(influence.id)
                if other_person:
                    rel: 'Relationship' = simulation.get_relationship(self.npc, other_person)
                    rel.modify_trust(influence.trust_change)
                    rel.modify_animosity(influence.animosity_change)
            return response.npc_response_to_player
        elif response.go_talk_to_intent:
            print("Go Talk To Intent")
            return response.npc_response_to_player
        elif response.new_rumor_intent:
            print("New Rumor Intent")
            self.hear_new_rumor(response.new_rumor_intent, simulation)
            return response.npc_response_to_player
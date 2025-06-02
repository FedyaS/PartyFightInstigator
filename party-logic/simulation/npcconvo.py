import random
from typing import List, TYPE_CHECKING

from simulation.settings import TICKS_PER_CONVO_TICK, RUMOR_SPREAD_CHANCE, MAX_VAL, RUMOR_BELIEVABILITY, \
    TRUST_DECREASE_ON_RUMOR_DISBELIEF, TRUST_INCREASE_ON_RUMOR_BELIEF, ANGER_INCREASE_PER_RUMOR_HARM, \
    ANGER_ANIMOSITY_FACTOR, ANGER_DECAY, ANGER_ADJUSTMENT_FACTOR, MIN_RUMOR_HARMFULNESS_TO_GROW_ANIMOSITY
from simulation.utils import create_id, apply_random_modifier, floor_ceiling_round

if TYPE_CHECKING:
    from simulation.simclass import Simulation
    from simulation.person import Person

class NPCConvo:
    def __init__(self, participants: List['Person'], id: str=None, max_tick_count=1000, randomize_stats=0):
        self.id = id or create_id()
        self.participants = participants
        self.max_tick_count = apply_random_modifier(max_tick_count, randomize_stats)
        self.tick_count = 0

        for person in participants:
            if person.active_conversation is not None:
                raise ValueError(f"Person {person.id} is already in a conversation")

            person.add_to_convo(self)

    def add_person(self, person: 'Person'):
        if person.active_conversation is not None:
            raise ValueError(f"Person {person.id} is already in a conversation")
        
        self.participants.append(person)
        person.add_to_convo(self)

    def remove_person(self, person: 'Person'):
        if person not in self.participants:
            raise ValueError(f"Person {person.id} is not in this conversation")

        self.participants.remove(person)
        person.remove_from_convo()

    def end_conversation(self):
        for person in self.participants:
            person.remove_from_convo()
        self.participants = []

    def choose_rumor_to_spread(self, simulation: 'Simulation'):
        spreadable_rumors = []  # [(Person, Rumor, Score)]

        # First, choose the rumor each person is going to spread and how likely they are to spread it
        for person in self.participants:
            personal_rumor_scores = []  # [(Rumor, Score)]

            for rumor in person.rumors:
                if person in rumor.subjects:
                    continue
                # Base score from gossip level and rumor plausibility
                score = person.gossip_level * rumor.plausibility

                # Adjust for trust with others in conversation
                avg_trust = 0
                count = 0
                for other in self.participants:
                    if other != person:
                        rel = simulation.get_relationship(person, other)
                        avg_trust += rel.trust if rel else 500
                        count += 1
                if count > 0:
                    avg_trust /= count
                    score *= (avg_trust / MAX_VAL)

                # Adjust for anger and rumor harmfulness
                anger_factor = person.anger / MAX_VAL
                harm_factor = rumor.harmfulness / MAX_VAL
                # Angry people spread harmful rumors; calm people spread less harmful ones
                anger_match = 1 + abs(anger_factor - harm_factor)
                score /= anger_match  # Closer anger-harm match increases likelihood

                personal_rumor_scores.append((rumor, score))

            if personal_rumor_scores:  # Only try to choose if there are rumors
                chosen_rumor, score = random.choices(
                    personal_rumor_scores,
                    weights=[score for _, score in personal_rumor_scores],
                    k=1
                )[0]
                spreadable_rumors.append((person, chosen_rumor, score))

        if not spreadable_rumors:  # If no one has rumors to spread
            return None, None, 0

        person, rumor, score = random.choices(
            spreadable_rumors,
            weights=[score for _, _, score in spreadable_rumors],
            k=1
        )[0]

        return person, rumor, score

    def spread_rumor(self, simulation: 'Simulation'):
        if RUMOR_SPREAD_CHANCE / MAX_VAL > random.random():
            spreader, rumor, score = self.choose_rumor_to_spread(simulation)
            if spreader and rumor:
                for person in self.participants:
                    if person != spreader:
                        relationship = simulation.get_relationship(spreader, person)
                        believed_chance = RUMOR_BELIEVABILITY * (
                                person.gullibility / MAX_VAL *
                                relationship.trust / MAX_VAL *
                                rumor.plausibility / MAX_VAL)
                        believed_it = believed_chance > random.random()

                        if believed_it:
                            relationship.modify_trust(TRUST_INCREASE_ON_RUMOR_BELIEF)
                            person.modify_anger(rumor.harmfulness * ANGER_INCREASE_PER_RUMOR_HARM)
                            person.rumors.add(rumor)

                            # Animosity towards subjects growths if the rumor was harmful
                            if (
                                    person not in rumor.subjects and
                                    rumor.harmfulness > MIN_RUMOR_HARMFULNESS_TO_GROW_ANIMOSITY
                            ):
                                for subject in rumor.subjects:
                                    rel = simulation.get_relationship(person, subject)
                                    rel.modify_animosity(rumor.harmfulness)
                                    rel.modify_trust(-rumor.harmfulness / 2)

                        else:
                            relationship.modify_trust(-TRUST_DECREASE_ON_RUMOR_DISBELIEF)

                        # If the rumor is about this person they get mad at the originators
                        if person in rumor.subjects:
                            person.modify_anger(rumor.harmfulness)
                            for originator in rumor.originators:
                                rel = simulation.get_relationship(person, originator)
                                rel.modify_animosity(rumor.harmfulness)
                                rel.modify_trust(-rumor.harmfulness / 2)

    def spread_emotions(self, simulation: 'Simulation'):
        # Initialize dictionary to accumulate anger influences
        total_delta_anger = {person: 0.0 for person in self.participants}

        # Process each unique pair of participants
        for i, person1 in enumerate(self.participants):
            for person2 in self.participants[i + 1:]:
                relationship = simulation.get_relationship(person1, person2)

                # Normalize anger and trust to [0,1]
                anger1_norm = person1.anger / 1000.0
                anger2_norm = person2.anger / 1000.0
                trust_norm = relationship.trust / 1000.0

                # Update animosity based on anger levels
                delta_animosity = ANGER_ANIMOSITY_FACTOR * (anger1_norm * anger2_norm - ANGER_DECAY)
                relationship.modify_animosity(delta_animosity)

                # Accumulate influence on anger based on trust and anger difference
                influence = trust_norm * (person2.anger - person1.anger)
                total_delta_anger[person1] += influence
                total_delta_anger[person2] -= influence

        # Update each person's anger based on accumulated influences
        num_participants = len(self.participants)
        for person in self.participants:
            if num_participants > 1:
                avg_delta = total_delta_anger[person] / (num_participants - 1)
                adjusted_delta = avg_delta * ANGER_ADJUSTMENT_FACTOR
                person.modify_anger(adjusted_delta)

    def tick(self, simulation):
        self.tick_count += 1
        for person in self.participants:
            person.active_conversation_ticks += 1

        if self.tick_count % TICKS_PER_CONVO_TICK == 0:
            self.spread_rumor(simulation)
            self.spread_emotions(simulation)
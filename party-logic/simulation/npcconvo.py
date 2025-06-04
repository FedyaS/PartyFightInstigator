import random
from typing import List, TYPE_CHECKING, Tuple

from simulation.settings import TICKS_PER_CONVO_TICK, RUMOR_SPREAD_CHANCE, MAX_VAL, RUMOR_BELIEVABILITY, \
    TRUST_DECREASE_ON_RUMOR_DISBELIEF, TRUST_INCREASE_ON_RUMOR_BELIEF, ANGER_INCREASE_PER_RUMOR_HARM, \
    ANGER_ANIMOSITY_FACTOR, ANGER_DECAY, ANGER_ADJUSTMENT_FACTOR, MIN_RUMOR_HARMFULNESS_TO_GROW_ANIMOSITY
from simulation.utils import create_id, apply_random_modifier, floor_ceiling_round

if TYPE_CHECKING:
    from simulation.simclass import Simulation
    from simulation.person import Person
    from simulation.rumor import Rumor

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

    def get_average_trust(self, person: 'Person', simulation: 'Simulation'):
        avg_trust = 500
        count = 1
        for other in self.participants:
            if other != person:
                rel = simulation.get_relationship(person, other)
                avg_trust += rel.trust if rel else 500
                count += 1
        avg_trust /= count
        return avg_trust

    def get_animosity_towards_subjects(self, person: 'Person', rumor: 'Rumor', simulation: 'Simulation'):
        total_animosity = 0
        for s in rumor.subjects:
            if person != s:
                rel = simulation.get_relationship(person, s)
                total_animosity += rel.animosity
        return total_animosity

    def get_rumor_known_score(self, rumor: 'Rumor'):
        all_people = len(self.participants)

        if all_people == 0:
            return 0

        knowing_people = -1
        for p in self.participants:
            if rumor in p.rumors:
                knowing_people += 1

        return 1000 * (1 - knowing_people/all_people)

    def calculate_person_rumor_spread_score(self, person: 'Person', rumor: 'Rumor', simulation: 'Simulation',
                                            average_trust: int):
        # People don't spread rumors about themselves
        if person in rumor.subjects:
            return 0

        fac1 = person.gossip_level
        fac2 = rumor.plausibility
        fac3 = average_trust
        fac4 = 1000 - (abs(person.anger - rumor.harmfulness))
        fac5 = 1000 if rumor.is_really_true else 0
        fac6 = self.get_animosity_towards_subjects(person, rumor, simulation)
        fac7 = self.get_rumor_known_score(rumor)

        return fac1 + fac2 + fac3 + fac4 + fac5 + fac6 + fac7

    def score_personal_rumors(self, person: 'Person', simulation: 'Simulation') -> List[Tuple['Person', 'Rumor', int]]:
        personal_rumor_scores = []
        average_trust = self.get_average_trust(person, simulation)

        for rumor in person.rumors:
            score = self.calculate_person_rumor_spread_score(person, rumor, simulation, average_trust)
            if score > 0:
                personal_rumor_scores.append((person, rumor, score))

        return personal_rumor_scores

    def choose_rumor_to_spread(self, simulation: 'Simulation'):
        spreadable_rumors = []  # [(Person, Rumor, Score)]

        for person in self.participants:
            spreadable_rumors += self.score_personal_rumors(person, simulation)

        if not spreadable_rumors:  # If no one has rumors to spread
            return None, None, 0

        person, rumor, score = random.choices(
            spreadable_rumors,
            weights=[score for _, _, score in spreadable_rumors],
            k=1
        )[0]

        return person, rumor, score

    def check_if_believed_rumor(self, person, rumor, relationship):
        believed_chance = RUMOR_BELIEVABILITY * (
                person.gullibility / MAX_VAL *
                relationship.trust / MAX_VAL *
                rumor.plausibility / MAX_VAL)
        print(f"believed chance: {believed_chance}")
        believed_it = random.random() < believed_chance
        return believed_it

    def spread_rumor(self, simulation: 'Simulation'):
        print(RUMOR_SPREAD_CHANCE/MAX_VAL)
        if random.random() < RUMOR_SPREAD_CHANCE / MAX_VAL:
            spreader, rumor, score = self.choose_rumor_to_spread(simulation)
            print(spreader)
            print(rumor)
            if spreader and rumor:
                for person in self.participants:
                    if person != spreader:
                        relationship = simulation.get_relationship(spreader, person)
                        rumor_is_about_this_person = person in rumor.subjects
                        believed_it = self.check_if_believed_rumor(person, rumor, relationship)

                        if rumor_is_about_this_person:
                            person.modify_anger(rumor.harmfulness)
                            relationship.modify_animosity(rumor.harmfulness)
                            relationship.modify_trust(-rumor.harmfulness / 2)
                            for originator in rumor.originators:
                                rel = simulation.get_relationship(person, originator)
                                rel.modify_animosity(rumor.harmfulness)
                                rel.modify_trust(-rumor.harmfulness / 2)

                        elif believed_it:
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

                        elif not believed_it:
                            relationship.modify_trust(-TRUST_DECREASE_ON_RUMOR_DISBELIEF)

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
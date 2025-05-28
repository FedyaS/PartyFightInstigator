import random
from simulation.person import Person
from simulation.simclass import Simulation
from simulation.rumor import Rumor
from simulation.settings import *

def create_demo_people():
    people = []
    
    # Create people with different personalities
    alice = Person(name="Alice", mbti="ENFJ", gullibility=300, gossip_level=800)
    bob = Person(name="Bob", mbti="ISTP", anger=200, convo_stay=700)
    charlie = Person(name="Charlie", mbti="ENTP", gullibility=600, gossip_level=400)
    dave = Person(name="Dave", mbti="INTJ", anger=100, convo_stay=300)
    
    people.extend([alice, bob, charlie, dave])
    return people

def create_demo_rumors(people):
    rumors = []
    
    # Create some juicy rumors
    rumors.append(Rumor(
        text="Alice secretly hates Dave's cooking",
        plausibility=700,
        harmfulness=300,
        subjects=[people[3]],  # Dave
        originators=[people[0]]  # Alice
    ))
    
    rumors.append(Rumor(
        text="Bob cheated on his last test",
        plausibility=400,
        harmfulness=600,
        subjects=[people[1]],  # Bob
        originators=[people[2]]  # Charlie
    ))
    
    rumors.append(Rumor(
        text="Charlie is planning to quit his job",
        plausibility=500,
        harmfulness=400,
        subjects=[people[2]],  # Charlie
        originators=[people[1]]  # Bob
    ))
    
    return rumors

class StateTracker:
    def __init__(self):
        self.prev_conversations = set()
        self.prev_rumors = {}  # person_id -> set of rumor texts
        self.prev_anger = {}   # person_id -> anger level
        self.prev_relationships = {}  # (p1_id, p2_id) -> (trust, animosity)
    
    def update(self, sim):
        # Store current state
        curr_conversations = set()
        curr_rumors = {}
        curr_anger = {}
        curr_relationships = {}
        
        # Track conversations
        for conv in sim.conversations.values():
            conv_key = tuple(sorted(p.id for p in conv.participants))
            curr_conversations.add(conv_key)
        
        # Track people's states
        for person in sim.people.values():
            curr_rumors[person.id] = {r.text for r in person.rumors}
            curr_anger[person.id] = person.anger
        
        # Track relationships
        for rel in sim.relationships.values():
            key = (rel.person1.id, rel.person2.id)
            curr_relationships[key] = (rel.trust, rel.animosity)
        
        # Find and print changes
        changes = []
        
        # New conversations
        new_convs = curr_conversations - self.prev_conversations
        if new_convs:
            changes.append("\nNEW CONVERSATIONS:")
            for conv_key in new_convs:
                names = [sim.people[pid].name for pid in conv_key]
                changes.append(f"  {' and '.join(names)} started talking")
        
        # Ended conversations
        ended_convs = self.prev_conversations - curr_conversations
        if ended_convs:
            changes.append("\nENDED CONVERSATIONS:")
            for conv_key in ended_convs:
                names = [sim.people[pid].name for pid in conv_key]
                changes.append(f"  {' and '.join(names)} stopped talking")
        
        # New rumors
        for person_id, rumors in curr_rumors.items():
            if person_id not in self.prev_rumors:
                new_rumors = rumors
            else:
                new_rumors = rumors - self.prev_rumors[person_id]
            if new_rumors:
                changes.append(f"\n{sim.people[person_id].name} learned new rumors:")
                for rumor in new_rumors:
                    changes.append(f"  - {rumor}")
        
        # Anger changes
        for person_id, anger in curr_anger.items():
            if person_id not in self.prev_anger or abs(anger - self.prev_anger[person_id]) > 50:
                changes.append(f"\n{sim.people[person_id].name}'s anger changed to {anger}")
        
        # Relationship changes
        for rel_key, (trust, animosity) in curr_relationships.items():
            if rel_key not in self.prev_relationships:
                changes.append(f"\nNew relationship between {sim.people[rel_key[0]].name} and {sim.people[rel_key[1]].name}:")
                changes.append(f"  Trust: {trust}, Animosity: {animosity}")
            else:
                prev_trust, prev_animosity = self.prev_relationships[rel_key]
                if abs(trust - prev_trust) > 50 or abs(animosity - prev_animosity) > 50:
                    changes.append(f"\nRelationship change between {sim.people[rel_key[0]].name} and {sim.people[rel_key[1]].name}:")
                    if abs(trust - prev_trust) > 50:
                        changes.append(f"  Trust changed from {prev_trust} to {trust}")
                    if abs(animosity - prev_animosity) > 50:
                        changes.append(f"  Animosity changed from {prev_animosity} to {animosity}")
        
        # Update previous state
        self.prev_conversations = curr_conversations
        self.prev_rumors = curr_rumors
        self.prev_anger = curr_anger
        self.prev_relationships = curr_relationships
        
        return changes

def print_full_state(sim):
    print("\n" + "="*50)
    print("SIMULATION STATE")
    print("="*50)
    
    # Print conversations
    print("\nACTIVE CONVERSATIONS:")
    for conv in sim.conversations.values():
        print(f"Conversation {conv.id}:")
        for person in conv.participants:
            print(f"  - {person.name} (Anger: {person.anger})")
    
    # Print people's states
    print("\nPEOPLE:")
    for person in sim.people.values():
        print(f"\n{person.name}:")
        print(f"  Anger: {person.anger}")
        print(f"  Active in conversation: {'Yes' if person.active_conversation else 'No'}")
        if person.rumors:
            print("  Rumors known:")
            for rumor in person.rumors:
                print(f"    - {rumor.text}")
    
    # Print relationships
    print("\nRELATIONSHIPS:")
    for rel in sim.relationships.values():
        print(f"\n{rel.person1.name} <-> {rel.person2.name}:")
        print(f"  Trust: {rel.trust}")
        print(f"  Animosity: {rel.animosity}")

def main():
    # Create simulation
    people = create_demo_people()
    sim = Simulation(people=people, min_convos=1, max_convos=2)
    
    # Add rumors to people
    rumors = create_demo_rumors(people)
    for rumor in rumors:
        rumor.originators[0].rumors.add(rumor)
    
    print("Simulation started! Press Enter to advance ticks, 'q' to quit")
    print_full_state(sim)
    
    state_tracker = StateTracker()
    state_tracker.update(sim)  # Initialize previous state
    
    while True:
        user_input = input("\nPress Enter to continue, 'q' to quit: ")
        if user_input.lower() == 'q':
            break
            
        sim.tick()
        changes = state_tracker.update(sim)
        
        if changes:
            print("\n" + "="*50)
            print("CHANGES THIS TICK:")
            print("="*50)
            for change in changes:
                print(change)
        else:
            print("\nNo significant changes this tick")

if __name__ == "__main__":
    main() 
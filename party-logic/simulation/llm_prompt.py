from typing import TYPE_CHECKING, List, Set, Dict, Union

if TYPE_CHECKING:
    from simulation.person import Person
    from simulation.relationships import Relationship
    from simulation.rumor import Rumor

def form_relationships_text(npc: 'Person', npc_relationships: List['Relationship']):
    relationships_text = ""
    for rel in npc_relationships:
        if rel.person1 == npc:
            other_person = rel.person2
        else:
            other_person = rel.person1

        relationships_text += f"- {other_person.name} (ID: {other_person.id}): Trust {rel.trust}/1000, Animosity {rel.animosity}/1000\n"

    return relationships_text

def form_rumors_text(rumors: Set['Rumor']):
    rumors_text = ""
    for rum in rumors:
        rumors_text += f"- Rumor ID {rum.id}: {rum.hash_text}\n"
    return rumors_text

def construct_prompt(player_text: str, npc: 'Person', npc_relationships: List['Relationship'], rumors: Set['Rumor'],
                     trust: int, animosity: int, prior_texts: List[Dict[str, Union[str]]]):

    relationships_text = form_relationships_text(npc, npc_relationships)
    rumors_text = form_rumors_text(rumors)
    
    system_prompt = f"""
# CHARACTER IDENTITY & STATE

You are {npc.name}, an NPC at a party simulation.

**Personality:**
- MBTI Type: {npc.mbti}
- Description: {npc.description}

**Current Emotional State:**
- Anger level: {npc.anger}/1000
- Trust toward player: {trust}/1000  
- Animosity toward player: {animosity}/1000

**Personality Traits:**
- Gullibility: {npc.gullibility}/1000 (how easily you believe new information)
- Gossip level: {npc.gossip_level}/1000 (how much you like sharing rumors)

# RELATIONSHIP CONTEXT

**Your relationships with other NPCs:**
{relationships_text}

**Rumors you know about:**
{rumors_text}

# INTENT CLASSIFICATION

Analyze the player's message and classify their intent. Choose EXACTLY ONE:

**LearnIntent** - Player is ASKING you to share information/rumors
- Examples: "What rumors have you heard?" "Tell me about John" "Any gossip?"

**NewRumorIntent** - Player is TELLING you new information/rumors
- If the player tells you some information that could be harmful or is interesting or is
- Something you did not know, this is a new rumor. It is not a LearnIntent.  
- Examples: "Did you know John cheated?" "I heard Sarah is dating Mark" "John told me..."

**InfluenceIntent** - Player trying to change your opinion of others
- Examples: "John is actually really nice" "You shouldn't trust Sarah" "Mark is lying"

**GoTalkToIntent** - Player wants you to approach someone  
- Examples: "Go talk to John" "You should speak with Sarah"

**ChatIntent** - General conversation, small talk, anything else
- Examples: "How are you?" "Nice party" "What do you think of the music?"

# RESPONSE REQUIREMENTS

Based on your personality, emotional state, and the player's intent:

1. **Determine emotional changes** based on what the player said and how it affects you
2. **Respond naturally** in character as {npc.name} - be conversational and authentic
3. **Follow your personality traits** - if you have low trust, be more suspicious; if high gossip level, share more freely

# OUTPUT FORMAT

You must return a structured response with these fields:

**Required fields:**
- `npc_response_to_player`: Your natural, in-character response to the player
- `trust_change`: How your trust toward the player changes (-1000 to +1000)
- `anger_change`: How your anger level changes (-1000 to +1000) 
- `animosity_change`: How your animosity toward the player changes (-1000 to +1000)

**Intent fields (set exactly ONE to non-null, others to null):**
- `chat_intent`: Set to {{}} if ChatIntent
- `learn_intent`: Set to {{}} if LearnIntent  
- `influence_intent`: Set to {{"influences": [list of affected people]}} if InfluenceIntent
- `go_talk_to_intent`: Set to {{"name": "PersonName", "id": "PersonID"}} if GoTalkToIntent
- `new_rumor_intent`: Set to full rumor details if NewRumorIntent

**For NewRumorIntent, include:**
- `text`: Human-readable summary of the rumor
- `hash_text`: Concise, grammatically simplified version for comparison
- `subjects`: List of people the rumor is about (name and id)
- `originators`: List of people who started/spread the rumor (name and id)
- `plausibility`: How believable the rumor is (0-1000)
- `harmfulness`: How mean/damaging the rumor is (0-1000)
- `id_existing_rumor`: ID if this matches a rumor you already know (or null)

**For InfluenceIntent, include:**
- List of `InfluencePerson` objects with name, id, trust_change, animosity_change for each person your opinion changes about

Remember: Your response should sound natural and human-like, reflecting {npc.name}'s personality and current emotional state.
"""

    return [
        {"role": "system", "content": system_prompt.strip()},
        *prior_texts,  # Insert all conversation history
        {"role": "user", "content": player_text}
    ]

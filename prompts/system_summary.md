# Party Fight Instigator - System Summary

## Core Architecture

The system simulates a party with NPCs who have relationships, spread rumors, and can talk to a player.

### Key Classes

**Simulation** (`simclass.py`)
- Central coordinator managing people, relationships, conversations, and rumors
- Runs tick-based simulation with automatic conversation management
- Handles player-NPC interactions

**Person** 
- NPCs with personality traits (MBTI, anger, gullibility, gossip_level)
- Can be in one active conversation at a time
- Store known rumors and relationship states

**Relationship**
- Bidirectional trust/animosity values between any two people
- Affects rumor believability and emotion spreading

**NPCConvo** (`npcconvo.py`)
- Group conversations between 2+ NPCs
- Handles rumor spreading and emotional contagion during conversations

**PlayerConvo**
- Individual conversation state between player and each NPC
- Tracks player-specific trust/animosity separate from NPC-NPC relationships

## Core Mechanics

### Tick System
Each simulation tick:
1. **Natural anger decay** - All NPCs gradually become less angry
2. **Conversation progression** - Active conversations advance their internal tick counters
3. **Fight detection** - Check if high anger + animosity should trigger fights
4. **Conversation management** - Randomly start/end conversations and add/remove participants

### NPC Conversations (NPCConvo)
When NPCs are in conversation, every few ticks:
1. **Rumor spreading** - NPCs share rumors based on gossip level, trust, and rumor scores
2. **Belief system** - Listeners may/may not believe rumors based on gullibility, trust, and plausibility
3. **Emotional consequences** - Rumors affect anger, trust, and animosity of subjects and listeners
4. **Emotion spreading** - NPCs influence each other's anger levels based on trust

### Player-NPC Interaction
Player can talk to any NPC via `talk_to_player()`:
1. **LLM prompt construction** - Builds detailed prompt with NPC personality, relationships, rumors, and conversation history
2. **Intent classification** - LLM categorizes player message (Learn, NewRumor, Influence, GoTalkTo, Chat)
3. **Response generation** - NPC responds in character with stat changes
4. **State updates** - Changes trust/animosity toward player and potentially other NPCs

## LLM Integration (`llm_prompt.py`)

The system constructs rich prompts containing:
- NPC personality (MBTI, description, current emotional state)
- All known relationships and rumors
- Player relationship status
- Intent classification requirements
- Structured response format expectations

The LLM must return responses with emotional state changes and properly categorized intents, enabling the system to update simulation state based on conversations.

## Current Limitations

- Fights are detected but not fully implemented
- No persistence between sessions
- Limited conversation depth tracking
- No advanced NPC goal/memory systems 
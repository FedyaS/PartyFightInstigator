# NPC Chat System Implementation

## Current State
- Text input/output with visual anger/trust feedback
- Intent-based system with classes: ChatIntent, LearnIntent, InfluenceIntent, GoTalkToIntent, NewRumorIntent
- LLMResponse includes intent field + npc_response_to_player
- Goal: Open-ended feel without restriction

## Required Player Capabilities
1. Learn about the NPC and potentially the NPC's rumors
2. Spread a new rumor to the NPC
3. Learn about the NPC relations to other NPCs
4. Influence the NPC view of somebody else
5. Send the NPC to go talk to someone

## Architecture Decision: Single vs Dual LLM Calls

### Recommendation: Single Call with Structured Output
- LLM outputs both intent classification AND response generation
- Forces explicit declaration of game state changes
- Maintains conversation flow
- Intents represent *state changes* not conversation topics

### Trade-off Question
Speed/cost vs reliability of state changes?

## Key Questions
1. Single LLM call vs dual LLM calls (intent detection + response generation)?
2. How to balance structure vs open-ended freedom?
3. Current player experience/interface?

## Options Being Explored
- Intent system architecture
- LLM call strategy
- Response generation approach 
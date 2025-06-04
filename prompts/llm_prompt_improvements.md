# LLM Prompt Improvement Plan

## Approach: Single File Restructure
Focus on improving llm_prompt.py only through better organization and clarity

## Current Prompt Issues
1. **Wall of Text**: Everything crammed together, hard to parse
2. **Buried Instructions**: Intent selection logic lost in personality description
3. **Unclear Intent Boundaries**: LearnIntent vs NewRumorIntent confusion
4. **Data Leakage**: conceal_score visible to NPCs
5. **Vague Output Specs**: No clear explanation of what response fields mean
6. **Overly Restrictive**: "concise" constraint limits natural dialogue

## Restructured Prompt Structure

### Section 1: Character Identity & State
- Name, MBTI, description
- Current emotional state (anger, trust, animosity)
- Personality traits (gullibility, gossip_level)

### Section 2: Relationship Context  
- Current relationships with other NPCs
- Known rumors (filtered, no internal metadata)

### Section 3: Intent Classification (CLEAR BOUNDARIES)
**LearnIntent**: Player is ASKING you to share information/rumors
- Examples: "What rumors have you heard?" "Tell me about John"

**NewRumorIntent**: Player is TELLING you new information/rumors  
- Examples: "Did you know John cheated?" "I heard Sarah is dating Mark"

**InfluenceIntent**: Player trying to change your opinion of others
**GoTalkToIntent**: Player wants you to approach someone  
**ChatIntent**: General conversation, small talk

### Section 4: Response Requirements
- Explain each output field clearly
- Remove "concise" constraint
- Emphasize natural, in-character dialogue

### Section 5: Output Format
- Clear JSON structure expectations
- Required vs optional fields
- Value ranges and meanings

## Key Changes
1. **Remove conceal_score from rumor data**
2. **Clearer intent definitions with examples**
3. **Sectioned prompt for better readability** 
4. **Detailed output field explanations**
5. **More natural response length** 
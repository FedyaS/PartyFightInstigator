# Party Fight Instigator - Player Interaction Improvements

## Current State Analysis
- Player chats with NPCs via LLM
- LLM returns trust/anger/animosity changes + potential new rumors
- NPCs have secrets with concealment scores
- NPCs spread rumors in conversations
- Goal: cause fights between NPCs

## Key Issues Identified
1. **Missing Integration**: LLM responses don't seem to feed back into simulation state
2. **Secret→Rumor Gap**: No clear path for learned secrets to become spreadable rumors
3. **Player Impact**: Unclear how player conversations actually affect the simulation

## Core Mechanics Questions
### Rumor Truthiness & Impact
- How to determine if rumor matches someone's secret (= true rumor)?
- True rumors should have higher plausibility, more damage
- Could use topic/tag matching between secrets and rumors

### Rumor Deduplication
- Same rumor spread to multiple NPCs = same rumor object
- Text similarity comparison on rumor essence?
- Hash normalized subjects + core claim?

### Secret-Rumor Linking Options
**Option A: Explicit Inventory**
- Player learns secrets as discrete items
- Can choose which secret to spread as rumor
- More strategic, game-like

**Option B: Organic Emergence** 
- Player conversations naturally create rumors
- System detects if rumor matches existing secrets
- More realistic but less controllable

## Implementation: Organic Rumor-Secret Matching

### Simple Approach (Quick to implement)
1. When LLM detects new rumor → extract core elements
2. Compare against all secrets in simulation
3. Matching criteria:
   - Extract people names from both
   - Normalize text (lowercase, remove filler)
   - Compare "core claim" using fuzzy string matching
   - If people overlap + text similarity > threshold → match found

### Advanced Approach 
- Use sentence embeddings for semantic comparison
- More accurate but requires additional dependencies

### LLM Comparison Approach (PREFERRED)
- Use LLM call to compare rumor against all secrets
- Input: rumor text + list of all secrets in simulation  
- Output: matching secret ID + confidence score (0-100)
- Benefits: handles rephrasing, simple to implement, very accurate
- Example prompt: "Does this rumor reveal any of these secrets? Which one and confidence level?"

### When to run comparison?
- Immediately when LLM detects rumor
- Check against all NPCs' secrets
- If match found: rumor gets "true" status, higher plausibility/damage

## SIMPLIFIED APPROACH: Secrets as Rumors

**Key Insight**: Make all secrets just be Rumor objects with subjects=[self]

### How it works:
- NPCSecret becomes Rumor with subjects=[person_who_has_secret]  
- High concealment = reluctance to share this rumor
- When player learns secret and spreads it → exact same rumor object spreads
- No comparison/matching needed - inherently "true" 
- Automatic deduplication since same rumor object everywhere

### Benefits:
- Eliminates entire matching system
- Much simpler code
- True rumors naturally have proper impact
- Same rumor spreads consistently

### Implementation:
- Track which rumors each person "knows" vs "owns as secret"
- Keep concealment score for reluctance to share
- Rest of rumor spreading logic stays the same

## Rumor Data Structure for LLM Comparison

### Option 1: Structured Fields + Filtering
```python
class Rumor:
    subjects: List[str]     # ["Alice", "Bob"]
    action_claim: str       # "cheated on" 
    full_text: str         # Complete rumor text
    topic: str             # "infidelity" (optional)
```

**Algorithm**: 
1. Filter existing rumors by overlapping subjects
2. LLM compares new rumor against just the filtered candidates

### Option 2: Rumor Signatures  
Convert rumors to standardized "signatures" for comparison:
- "Bob is secretly wealthy" → [Bob] + "wealth secret"
- "I heard Bob has money hidden" → [Bob] + "wealth secret"  

**Benefits**: Makes LLM comparison much clearer than full text

## Questions to Explore
- Where does LLM response get applied to simulation?
- When NPC shares secret, does player get it as spreadable rumor?
- How do player-introduced rumors enter NPC rumor spreading system? 
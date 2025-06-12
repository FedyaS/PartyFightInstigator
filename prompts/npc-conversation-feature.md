# NPC Conversation Feature Requirements

## Core Features

### 1. TALK TO NPC Button

- Location: Top right of NPCCard
- Action: Sets activeNpcId to current NPC

### 2. Active Conversation Display

- Location: Below stats, above navigation arrows in NPCCard
- Shows: "Active Conversation:" header

#### If NPC not in conversation (conversation_id is null):

- Display: "{NAME} is not talking to anybody"

#### If NPC is in conversation:

- Display: "{NAME} is currently talking with {Name1}, {Name2}, {Name3}, etc."
- Participant names are clickable
- Clicking navigates to that NPC's card (updates currentNPCIndex)
- Does NOT set activeNpcId (conversation doesn't start)
- Animated dots after participant list (typing effect)

### 3. Data Structure Changes

- Refactor npcConversations from array to dictionary: `{ id: ConversationObject }`
- Enables easier lookup by conversation_id

# NPC Conversation Feature - Implementation Plan

## Precise Changes Required

### 1. GameLayout.jsx

**Change**: Pass `setActiveNpcId` to `AttendeesView`

```jsx
// Line 25: Change from
<AttendeesView />
// To:
<AttendeesView setActiveNpcId={setActiveNpcId} />
```

### 2. AttendeesView.jsx

**Changes**:

- Accept `setActiveNpcId` prop
- Pass required props to NPCCard including navigation handler

```jsx
// Line 6: Update function signature
function AttendeesView({ setActiveNpcId }) {

// Add navigation handler for participant clicks
const handleNavigateToNPC = (npcId) => {
  const npcIndex = npcArray.findIndex(npc => npc.id === npcId);
  if (npcIndex !== -1) {
    setCurrentNPCIndex(npcIndex);
  }
};

// Line 43: Update NPCCard props
<NPCCard
  npc={currentNPC}
  onNext={handleNext}
  onPrev={handlePrev}
  setActiveNpcId={setActiveNpcId}
  onNavigateToNPC={handleNavigateToNPC}
/>
```

### 3. NPCCard.jsx

**Changes**:

- Accept new props: `setActiveNpcId`, `onNavigateToNPC`
- Add Redux selector for npcConversations
- Add TALK TO NPC button in header
- Add Active Conversation section between stats and navigation
- Create conversation display logic with animated dots

```jsx
// Add imports
import { useSelector } from "react-redux";
import { useEffect, useState } from "react";

// Update function signature
function NPCCard({ npc, onNext, onPrev, setActiveNpcId, onNavigateToNPC }) {

// Add Redux selectors
const npcs = useSelector((state) => state.game.npcs);
const npcConversations = useSelector((state) => state.game.npcConversations);

// Add animated dots state
const [dots, setDots] = useState("...");

// Add dots animation effect
useEffect(() => {
  const interval = setInterval(() => {
    setDots(prev => prev.length >= 3 ? "." : prev + ".");
  }, 500);
  return () => clearInterval(interval);
}, []);

// Add TALK TO NPC button in npc-header-content (top right)
// Add Active Conversation section after npc-card-stats
// Add conversation display logic
```

### 4. gameSlice.js

**Change**: Refactor npcConversations from array to dictionary

```js
// Line 48: Change from
npcConversations: [
  // { id: string, participants: string[], memo: string }
],

// To:
npcConversations: {
  // id: { id: string, participants: string[], memo: string }
},

// Update reducer logic in updateGameState to handle dictionary structure
```

## Component Structure Changes

### NPCCard Layout:

1. npc-header (existing)
   - npc-header-content (existing)
     - image + name (existing)
     - **NEW**: TALK TO NPC button (top right)
2. npc-card-stats (existing)
3. **NEW**: npc-conversation-status section
4. npc-card-navigation (existing)

### Conversation Display Logic:

- If `npc.conversation_id` is null: "{name} is not talking to anybody"
- If conversation exists: "{name} is currently talking with {clickable names}{animated dots}"

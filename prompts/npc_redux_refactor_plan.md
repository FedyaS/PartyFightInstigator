# NPC Redux Refactor Plan

## Concrete Implementation Changes

### 1. gameSlice.js Changes

**Change npcs from array to dictionary:**

```js
// BEFORE:
npcs: []

// AFTER:
npcs: {
  "npc1": { id: "npc1", name: "CEO", ... },
  "npc2": { id: "npc2", name: "Manager", ... }
}
```

**Update reducers to work with dictionary:**

- `sendPlayerMessage`: Change `state.npcs.find()` to `state.npcs[npcId]`
- `updatePlayerConversation`: Same change
- `updateGameState`: Handle npcs as object

**Add mock data in initialState:**

```js
npcs: {
  "ceo": {
    id: "ceo",
    name: "CEO",
    relationship_score: 25,
    anger: 57,
    personality: "demanding",
    gullibility: 30,
    conversation_id: null,
    playerConversation: {
      last_npc_message: "Hello! I am the CEO. Ask me anything.",
      last_player_message: null,
      last_message_is: "NPC",
      NPC_is_thinking: false
    }
  },
  "manager": {
    id: "manager",
    name: "Manager",
    relationship_score: 60,
    anger: 20,
    personality: "friendly",
    gullibility: 70,
    conversation_id: null,
    playerConversation: {
      last_npc_message: "Hey there! How's the party going?",
      last_player_message: null,
      last_message_is: "NPC",
      NPC_is_thinking: false
    }
  }
}
```

### 2. GameLayout.jsx Changes

**Add state for active NPC and pass as prop:**

```js
// Add to component:
const [activeNpcId, setActiveNpcId] = useState("ceo");

// Update ConversationView line:
<ConversationView activeNpcId={activeNpcId} />;
```

### 3. ConversationView.jsx Changes

**Remove all local state except playerInputText:**

- Remove: npcMessage, playerMessage, angerLevel, trustLevel
- Keep: playerInputText, isPlayerInputLocked, animationDirection

**Add Redux connections:**

```js
// Add props
function ConversationView({ activeNpcId }) {
  const dispatch = useDispatch();
  const activeNpc = useSelector(state => state.game.npcs[activeNpcId]);

  // Derived values from Redux:
  const npcMessage = {
    text: activeNpc?.playerConversation.last_npc_message || "",
    isLoading: activeNpc?.playerConversation.NPC_is_thinking || false
  };
  const playerMessage = activeNpc?.playerConversation.last_player_message
    ? { text: activeNpc.playerConversation.last_player_message }
    : null;
  const angerLevel = activeNpc?.anger || 0;
  const trustLevel = activeNpc?.relationship_score || 0;
```

**Update handleSendMessage:**

```js
const handleSendMessage = () => {
	if (playerInputText.trim() === "" || isPlayerInputLocked) return;

	setPlayerInputText("");
	setIsPlayerInputLocked(true);
	setAnimationDirection("up");

	dispatch(
		sendPlayerMessage({
			npcId: activeNpcId,
			message: playerInputText,
		})
	);

	// Mock response (replace with real backend call later)
	setTimeout(() => {
		dispatch(
			updatePlayerConversation({
				npcId: activeNpcId,
				last_npc_message: `I received: "${playerInputText}". Interesting!`,
				last_message_is: "NPC",
				NPC_is_thinking: false,
			})
		);
		setIsPlayerInputLocked(false);
		setAnimationDirection("down");
	}, 2000);
};
```

### 4. Selector Optimization

**ConversationView subscribes to all npcs** - React-Redux will only re-render if the specific NPC data changes due to shallow equality checks. No need for complex memoization initially.

### File Change Summary:

- **gameSlice.js**: Restructure npcs, update 3 reducers, add mock data
- **GameLayout.jsx**: Add activeNpcId state, pass as prop
- **ConversationView.jsx**: Remove local state, add Redux hooks, update message handler

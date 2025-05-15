# NPC Chat Feature Implementation Plan

## Phase 1: Initial Brainstorming & Layout

### GameLayout.jsx Modifications
- Goal: Simplify to two main sections: Main Game Area and Graph Area (right).
- Current sections: Status Bar, Main Content (Sidebar, Content Area), Graph Section.
- Decision:
    - Status Bar: Stays as is.
    - The existing `sidebar` ("Chats / NPC Info") and `content-area` ("SVG or Game Content Here") will be replaced by the new `ConversationView` component.
    - The `graph-section` (Graph) remains on the right.

### New Component: ConversationView.jsx
- Purpose: Handle the visual and interactive elements of the NPC conversation.
- Location: To be rendered in the main content area of `GameLayout.jsx`, replacing the old sidebar and content area.
- Key Visual Elements:
    - NPC Image (`public/assets/ceo.png`): Positioned on the left.
    - NPC Speech Bubble: Positioned to the right of the NPC image. May be centered on the screen (TBD during implementation).
    - Player Speech Bubble: Positioned above the player input text box.
    - Player Input Text Box (futuristic design):
        - Rounded shape.
        - Text appears larger while player is typing.
        - Potential animation for typed words (e.g., subtle glow, letter pop-in).
        - Standard text input functionality (cursor, selection, backspace).
    - Send Button (using `public/icons/send.svg`)
    - Lock icon for input box (using `public/icons/lock.svg`)
- State Management:
    1.  NPC speech content (text, empty, loading)
    2.  Player's last said message (text or empty)
    3.  Player input lock state (boolean)

## Open Questions/Discussion Points:
- Fate of existing "Chats / NPC Info" sidebar? -> Replaced by ConversationView
- Fate of existing "Status Bar"? -> Stays
- Specifics of "futuristic looking text input box" design? -> Rounded, large text on type, potential word animation. Standard functionality.
- How will the NPC image and speech bubble be positioned relative to each other? -> Image left, bubble right (possibly centered on screen).
- How will the player's speech bubble be positioned relative to the input box? -> Directly above.
- Error handling for NPC responses?
- Initial state of the conversation when the component loads?

### SVG/Asset Requirements:
- Speech bubbles: Will be dynamically sized (likely CSS/HTML), not static SVGs.
- SVGs created:
    - Send button icon: `public/icons/send.svg`
    - Lock icon for the input box: `public/icons/lock.svg`
- Potentially, decorative elements for the futuristic text input if not handled by CSS alone. 
    - Details on text size change (permanent while in input, or only during active typing?).
    - Specifics of word animation desired. 
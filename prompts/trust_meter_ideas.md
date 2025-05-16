# Trust Meter Implementation Ideas

## Initial Concept
- User wants to implement a trust meter (1-100).
- Has an SVG for the meter.
- Arrow should turn and point according to the number.

## Questions to Clarify
- How does the SVG visually represent the trust level with the arrow? (e.g., dial, color change)
- Where should the trust meter be placed in the `ConversationView`?
- How will the trust value be determined and updated? 

## Updated Plan (Based on User Feedback)

### Trust Meter Visuals & Placement
- **Appearance:** Futuristic sleek dial with numbers 0, 20, 40, 60, 80, 100.
- **Arrow:** Rotates to point to the current trust number position.
- **Text:** "TRUST" label below the meter in an appropriate font.
- **Placement:** In the `npc-area`, on the right side of the NPC's message/speech bubble. The `emotion-section` (anger bar) will be below the row containing the message and trust meter.
  - Current `npc-area` structure: `Image | [Speech Bubble / Emotion Bar]`
  - New `npc-area` structure: `Image | [Speech Bubble | Trust Meter] / [Emotion Bar]` (conceptual)

### State Management
- A new `useState` variable: `trustLevel` (0-100).

### Further Questions
- **Initial Value & Change:** What is the starting `trustLevel`? How does it change per message (e.g., increase by X, decrease by Y)?
- **Rotation Range:** What is the total angle of rotation for the arrow (e.g., 0 trust at -90deg, 100 trust at +90deg, for a 180deg sweep)?
- SVG Structure: Will the provided SVG have a separately controllable arrow element for CSS rotation?
- Trust Logic: How will `trustLevel` be calculated and updated during the conversation?

### SVG Requirements for Implementation
- **Option 1 (Separate SVGs):**
  1. `dial.svg`: Static background with numbers (0, 20, 40, 60, 80, 100) and dial markings. (User has provided as `public/icons/dial.svg`)
  2. `arrow.svg`: The pointer, designed for rotation around its base. (User has provided as `public/icons/dial-pointer.svg`)
- **Option 2 (Combined SVG):**
  - A single SVG file where the dial and the arrow are distinct elements (e.g., paths or groups with unique IDs) to allow the arrow to be targeted and rotated independently via CSS/JS.

### State Management & Logic (Updated)
- A new `useState` variable: `trustLevel` (0-100).
- **Update Logic:** For now, `trustLevel` will change with each message, following similar rules to `angerLevel`.

### Next Steps (Pending User Feedback)
- Clarify current SVG structure.
- Define specific logic for `trustLevel` updates (initial value, change per message).
- Define arrow rotation range. 
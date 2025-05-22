# Graph Section Implementation Plan

## Components Needed
1. ViewSwitcher (segmented control with glow effects)
2. MapView (placeholder with bg image)
3. AttendeesView
4. NPCCard
   - Image (circular)
   - Name
   - Stats (trust, anger, stat3, stat4) - all visible
   - Description
   - Friends list (clickable)
   - Foes list (clickable)
   - Navigation arrows

## Styling Considerations
- Follow existing dark theme with blue accents
- Glow effects for cards and segmented control
- Consistent font usage
- Responsive layout within graph-section
- Smooth transitions between views (fade)

## Implementation Details
1. Use CSS transitions for view switching
2. Implement segmented control with active state glow
3. All stats visible in card layout
4. Keyboard navigation for card switching

## Questions to Consider
1. Should we use a state management solution for NPC data?
2. How should we handle the circular image cropping?
3. Should we implement keyboard navigation for the entire section?
4. Do we need animations for view switching? 
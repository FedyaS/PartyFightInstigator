import React, { useState, useEffect, useMemo } from 'react';

const ANIMATION_INTERVAL = 300; // ms
const MAX_LAYERS = 10; // Max number of layers in the cone
const DOT_RADIUS_VIEWBOX = 0.04; // Made dots smaller
const CONE_WIDTH_RATIO = 0.7; // Ratio of cone base width to cone length (height)
const SQRT2_INV = Math.sqrt(0.5);

// Generates base coordinates for a canonical cone
// Tip at (0,0), opens along positive Y-axis (y from 0 to 1)
// X-coordinates are relative to the Y-axis, creating the cone shape.
const generateBaseConeDots = (numLayers, coneWidthRatio) => {
  const dots = [];
  let idCounter = 1;
  if (numLayers === 0) return [];

  for (let l = 1; l <= numLayers; l++) { // l is the layer number (1 to numLayers)
    const y_norm = (numLayers === 1 && l === 1) ? 0 : (l - 1) / (numLayers - 1);
    for (let i = 0; i < l; i++) { 
      let x_norm_offset;
      if (l === 1) { 
        x_norm_offset = 0;
      } else {
        const widthAtThisLayer = y_norm * coneWidthRatio;
        x_norm_offset = (i / (l - 1) - 0.5) * widthAtThisLayer;
      }
      
      dots.push({
        id: `vcd${idCounter++}`,
        x_offset: x_norm_offset, 
        y_progress: y_norm,     
        layer: l,
      });
    }
  }
  return dots;
};

const VoiceDotCone = ({ size = 100, animationDirection = 'none', color = 'cyan', animationCycles = 0 }) => {
  const [animationStep, setAnimationStep] = useState(0); 
  const [completedCyclesCount, setCompletedCyclesCount] = useState(0);

  const allPossibleDots = useMemo(() => generateBaseConeDots(MAX_LAYERS, CONE_WIDTH_RATIO), []);

  useEffect(() => {
    setAnimationStep(0);
    setCompletedCyclesCount(0);
  }, [animationDirection]);

  useEffect(() => {
    if (animationDirection === 'none') {
      setAnimationStep(0);
      setCompletedCyclesCount(0);
      return;
    }

    // If the target number of cycles has been completed, ensure we are visually in the paused state and stop further animation.
    if (animationCycles > 0 && completedCyclesCount >= animationCycles) {
      if (animationStep !== MAX_LAYERS + 1) {
        setAnimationStep(MAX_LAYERS + 1); // Snap to paused state if not already there.
      }
      return; // Stop: Do not schedule a new timer.
    }

    // Otherwise, schedule the next animation step.
    const timer = setTimeout(() => {
      setAnimationStep(prevStep => {
        if (prevStep === MAX_LAYERS + 1) { // Currently in pause state, a cycle is about to end.
          const newCompletedCycles = completedCyclesCount + 1; // Tentative new count.
          setCompletedCyclesCount(newCompletedCycles); // Commit the increment.

          if (animationCycles > 0 && newCompletedCycles >= animationCycles) {
            // This cycle (which just incremented the count) is the Nth cycle or more. Stop by remaining paused.
            return MAX_LAYERS + 1;
          } else {
            // Continue looping.
            return 0;
          }
        } else {
          // Normal progression through growing steps or from 0 to 1.
          // This will take it up to MAX_LAYERS + 1, then the above case handles the cycle end.
          return prevStep + 1;
        }
      });
    }, ANIMATION_INTERVAL);

    return () => clearTimeout(timer);
    // MAX_LAYERS is a const, not prop/state, so not strictly needed in deps if not changing.
    // allPossibleDots is memoized and stable.
  }, [animationDirection, animationCycles, completedCyclesCount, animationStep]); 

  const visibleDots = useMemo(() => {
    if (animationDirection === 'none') {
      return [];
    }
    let layersToShow;
    if (animationStep === 0) { 
      layersToShow = 0;
    } else if (animationStep <= MAX_LAYERS) { 
      layersToShow = animationStep;
    } else { // animationStep === MAX_LAYERS + 1: Pause phase
      layersToShow = MAX_LAYERS;
    }
    if (layersToShow === 0) {
      return [];
    }
    return allPossibleDots.filter(dot => dot.layer <= layersToShow);
  }, [animationDirection, animationStep, allPossibleDots]); // MAX_LAYERS influences allPossibleDots implicitly

  const vbMin = -0.2;
  const vbDim = 1.4; 

  return (
    <svg
      width={size}
      height={size} 
      viewBox={`${vbMin} ${vbMin} ${vbDim} ${vbDim}`}
      style={{ overflow: 'visible' }}
    >
      <g transform={`scale(1, -1) translate(0, ${-vbDim}) rotate(0 ${vbDim/2} ${vbDim/2})`}>
        {/* The Y-axis is now flipped. (0,0) in this g is top-left of viewBox. Positive Y goes down.*/}
        {/* We want our cone's logical (0,0) bottom-left, (1,1) top-right for calculation convenience.*/}
        {/* So, we'll map our [0,1]x[0,1] cone into the viewBox, adjusting for flipped Y. */}
        {/* The center of our logical 1x1 drawing area will be (0.5, 0.5) */}
        {/* This means we need to shift our coordinates before they are drawn. */}
        {/* Let's adjust cx, cy in the dot mapping logic instead to map to viewBox after the g transform. */}
        {visibleDots.map((dot) => {
          const t = dot.y_progress; 
          const offsetX = dot.x_offset; 

          let final_cx, final_cy;
          let cone_tip_x, cone_tip_y;
          let axis_vec_x, axis_vec_y;
          let perp_vec_x, perp_vec_y;

          // All coordinates here are conceptual, in a [0,1] x [0,1] space where Y is up.
          // The final transform on <g> will place this into the SVG viewport.
          if (animationDirection === 'up') {
            // Tip at Bottom-Right (logical 1,0), opens towards Top-Left (logical 0,1)
            cone_tip_x = 1; cone_tip_y = 0;
            axis_vec_x = -SQRT2_INV; axis_vec_y = SQRT2_INV; // Normalized vector from BR to TL
            perp_vec_x = SQRT2_INV; perp_vec_y = SQRT2_INV; // Normalized perpendicular to axis
          } else { // "down"
            // Tip at Top-Left (logical 0,1), opens towards Bottom-Right (logical 1,0)
            cone_tip_x = 0; cone_tip_y = 1;
            axis_vec_x = SQRT2_INV; axis_vec_y = -SQRT2_INV; // Normalized vector from TL to BR
            perp_vec_x = SQRT2_INV; perp_vec_y = SQRT2_INV; // Normalized perpendicular to axis
          }

          // Project point onto axis and add perpendicular offset
          final_cx = cone_tip_x + t * axis_vec_x + offsetX * perp_vec_x;
          final_cy = cone_tip_y + t * axis_vec_y + offsetX * perp_vec_y;
          
          // Now, map these [0,1]-ish coordinates into the viewBox. 
          // The <g> transform flips Y and translates. We want our cone to fill a logical 1x1 square
          // centered within the viewBox (vbMin to vbMin+vbDim).
          // Let the logical 1x1 area be from viewBox X=0.2, Y=0.2 to X=1.2, Y=1.2 (considering Y flip later)
          const logicalAreaOriginX = (vbDim - 1) / 2; // e.g. (1.4-1)/2 = 0.2
          const logicalAreaOriginY = (vbDim - 1) / 2;

          const mapped_cx = logicalAreaOriginX + final_cx;
          const mapped_cy = logicalAreaOriginY + final_cy; 
          // mapped_cy is still Y-up. The main <g> transform handles the flip.

          return (
            <circle
              key={dot.id}
              cx={mapped_cx}
              cy={mapped_cy} 
              r={DOT_RADIUS_VIEWBOX * vbDim} 
              fill={color}
            />
          );
        })}
      </g>
    </svg>
  );
};

export default VoiceDotCone; 
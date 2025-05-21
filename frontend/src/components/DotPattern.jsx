import React, { useState, useEffect } from 'react';

const DOT_RADIUS = 0.15;
const ANIMATION_INTERVAL = 700; // ms

const allDots = [
  { id: 'd1', x: 0, y: 0, group: 'middle' },
  { id: 'd2', x: 0.7, y: -1, group: 'bottom' },
  { id: 'd3', x: -0.7, y: 1, group: 'top' },
  { id: 'd4', x: 2, y: 0.25, group: 'middle' },
  { id: 'd5', x: 2.2, y: -1, group: 'bottom' },
  { id: 'd6', x: 1.2, y: 1, group: 'top' },
  { id: 'd7', x: -1.2, y: -1, group: 'bottom' },
  { id: 'd8', x: -2, y: -0.25, group: 'middle' },
  { id: 'd9', x: -2.2, y: 1, group: 'top' },
];

const DotPattern = ({ size = 100, animationDirection = 'none' }) => {
  const [animationStep, setAnimationStep] = useState(0); // 0: all gray, 1: G1, 2: G1+G2, 3: G1+G2+G3

  useEffect(() => {
    if (animationDirection === 'none') {
      setAnimationStep(0);
      return;
    }

    const timer = setTimeout(() => {
      setAnimationStep(prevStep => (prevStep + 1) % 4); // Cycle through 0, 1, 2, 3
    }, ANIMATION_INTERVAL);

    return () => clearTimeout(timer);
  }, [animationDirection, animationStep]);

  const getDotColor = (dot) => {
    if (animationDirection === 'none' || animationStep === 0) {
      return 'black';
    }

    const groupOrder = animationDirection === 'up' ? ['bottom', 'middle', 'top'] : ['top', 'middle', 'bottom'];
    
    let isLit = false;
    // Check if the dot's group should be lit based on the current animation step
    if (animationStep >= 1 && dot.group === groupOrder[0]) isLit = true;
    if (animationStep >= 2 && dot.group === groupOrder[1]) isLit = true;
    if (animationStep >= 3 && dot.group === groupOrder[2]) isLit = true;
    
    // If it's step 3, all groups defined in groupOrder are lit.
    // To ensure only the specified groups are lit cumulatively:
    if (animationDirection === 'up') {
        if (dot.group === 'bottom' && animationStep >= 1) return 'cyan';
        if (dot.group === 'middle' && animationStep >= 2) return 'cyan';
        if (dot.group === 'top' && animationStep >= 3) return 'cyan';
    } else if (animationDirection === 'down') {
        if (dot.group === 'top' && animationStep >= 1) return 'cyan';
        if (dot.group === 'middle' && animationStep >= 2) return 'cyan';
        if (dot.group === 'bottom' && animationStep >= 3) return 'cyan';
    }

    return 'black';
  };

  // viewBox settings: minX, minY, width, height
  // Dot X-coords range from -2.2 to 2.2 (width 4.4)
  // Dot Y-coords range from -1 to 1 (height 2)
  // Add slight padding for dot radius: 0.1 on each side for range, 0.2 for dimension
  const viewBoxWidth = 4.4 + DOT_RADIUS * 2;
  const viewBoxHeight = 2 + DOT_RADIUS * 2;
  const minX = -2.2 - DOT_RADIUS;
  const minY = -1 - DOT_RADIUS; // This minY is for the coordinate system after y-inversion

  return (
    <svg
      width={size}
      height={size * (viewBoxHeight / viewBoxWidth)} // Maintain aspect ratio
      viewBox={`${minX} ${minY} ${viewBoxWidth} ${viewBoxHeight}`}
    //   style={{ border: '1px solid lightgray', overflow: 'visible' }} // Added for visibility
    >
      {/* Apply a transform to make positive Y point upwards, matching problem's coordinate system */}
      <g transform="scale(1, -1)">
        {allDots.map((dot) => (
          <circle
            key={dot.id}
            cx={dot.x}
            cy={dot.y} // Use original y; transform handles the inversion for SVG
            r={DOT_RADIUS}
            fill={getDotColor(dot)}
          />
        ))}
      </g>
    </svg>
  );
};

export default DotPattern; 
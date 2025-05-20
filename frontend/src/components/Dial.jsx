import React, { useState, useEffect } from 'react';

function mapValueToAngle(value) {
    // Ensure value is within 0-100 range, as trustLevel is.
    const v = Math.min(100, Math.max(0, value));

    if (v >= 0 && v <= 25) {
      return -2.16 * v + 54 + 360;
    } else if (v <= 40) { // This implies v > 25
      return ((v - 26) / (26 - 40)) * (359 - 336) + 359;
    } else if (v <= 60) { // This implies v > 40
      return ((v - 40) / (60 - 40)) * (232 - 336) + 336;
    } else if (v <= 100) { // This implies v > 60
      return ((v - 60) / (100 - 60)) * (154 - 232) + 232;
    }
    // Fallback for any case not covered, though clamping should prevent this.
    // If v is exactly 25, first branch. If v is 0, first branch.
    // If v is 100, last branch.
    return 0; // Default return if something unexpected happens
}

function Dial({ trustLevel }) {
  const dialAssetUrl = '/icons/dial.svg';
  const pointerAssetUrl = '/icons/dial-pointer.svg';

  const [svgFilter, setSvgFilter] = useState('');
  const P_RED =   { inv: 30, sep: 90, sat: 6000, hue: 350, bri: 90, con: 120 };
  const P_YELLOW = { inv: 80, sep: 50, sat: 3000, hue: 350, bri: 100, con: 100 };
  const P_GREEN =  { inv: 48, sep: 79, sat: 2476, hue: 86,  bri: 118, con: 119 };

  const interpolateValues = (v1, v2, factor) => v1 * (1 - factor) + v2 * factor;  

  useEffect(() => {
    const calculateFilter = () => {
      let currentTrust = trustLevel;
      if (currentTrust < 0) currentTrust = 0;
      if (currentTrust > 100) currentTrust = 100;

      let params;
      if (currentTrust < 50) {
        const factor = currentTrust / 50;
        params = {
          inv: interpolateValues(P_RED.inv, P_YELLOW.inv, factor),
          sep: interpolateValues(P_RED.sep, P_YELLOW.sep, factor),
          sat: interpolateValues(P_RED.sat, P_YELLOW.sat, factor),
          hue: interpolateValues(P_RED.hue, P_YELLOW.hue, factor),
          bri: interpolateValues(P_RED.bri, P_YELLOW.bri, factor),
          con: interpolateValues(P_RED.con, P_YELLOW.con, factor),
        };
      } else {
        const factor = (currentTrust - 50) / 50;
        params = {
          inv: interpolateValues(P_YELLOW.inv, P_GREEN.inv, factor),
          sep: interpolateValues(P_YELLOW.sep, P_GREEN.sep, factor),
          sat: interpolateValues(P_YELLOW.sat, P_GREEN.sat, factor),
          hue: interpolateValues(P_YELLOW.hue, P_GREEN.hue, factor),
          bri: interpolateValues(P_YELLOW.bri, P_GREEN.bri, factor),
          con: interpolateValues(P_YELLOW.con, P_GREEN.con, factor),
        };
      }
      return `invert(${Math.round(params.inv)}%) sepia(${Math.round(params.sep)}%) saturate(${Math.round(params.sat)}%) hue-rotate(${Math.round(params.hue)}deg) brightness(${Math.round(params.bri)}%) contrast(${Math.round(params.con)}%)`;
    };
    setSvgFilter(calculateFilter());
  }, [trustLevel, P_RED, P_YELLOW, P_GREEN]); // Added dependencies


  // Overall container size
  const containerWidth = 185;
  const containerHeight = 132;
  const containerMarginBottom = '2px';

  // Center of the dial
  const dialCenterX = 92;
  const dialCenterY = 79;

  // Original pointer dimensions
  const originalPointerWidth = 200;
  const originalPointerHeight = 84;
  
  // Original pivot point in pointer's coordinate space
  const originalPivotX = 195;
  const originalPivotY = 59;

  // Scale factor to fit pointer within container
  const scaleFactor = Math.min(
    (containerWidth * 0.3) / originalPointerWidth,
    (containerHeight * 0.3) / originalPointerHeight
  );

  // Scaled pointer dimensions
  const pointerImgWidth = originalPointerWidth * scaleFactor;
  const pointerImgHeight = originalPointerHeight * scaleFactor;

  // Scaled pivot point
  const pivotX_in_pointerSvg = originalPivotX * scaleFactor;
  const pivotY_in_pointerSvg = originalPivotY * scaleFactor;

  // Calculate top-left position for the pointer SVG so its pivot aligns with the dial's center
  const pointerSvgLeft = dialCenterX - pivotX_in_pointerSvg;
  const pointerSvgTop = dialCenterY - pivotY_in_pointerSvg;

  const angle = mapValueToAngle(trustLevel);
  // The original Dial.jsx used `rotate(${-angle}deg)`.
  const rotationTransform = `rotate(${-angle}deg)`;

  return (
    <div
      style={{
        position: 'relative',
        width: `${containerWidth}px`,
        height: `${containerHeight}px`,
        marginBottom: containerMarginBottom,
        // border: '1px dashed grey', // For layout debugging
      }}
    >
      {/* Dial Background Image */}
      <img
        src={dialAssetUrl}
        alt="Trust Dial Background"
        style={{
          width: '100%',
          height: '100%',
          filter: svgFilter,
          position: 'absolute',
          top: '0',
          left: '0',
        }}
      />

      {/* SVG container for the Pointer Image */}
      <svg
        width={pointerImgWidth}
        height={pointerImgHeight}
        viewBox={`0 0 ${originalPointerWidth} ${originalPointerHeight}`}
        style={{
          position: 'absolute',
          left: `${pointerSvgLeft}px`,
          top: `${pointerSvgTop}px`,
          transformOrigin: `${pivotX_in_pointerSvg}px ${pivotY_in_pointerSvg}px`,
          transform: rotationTransform,
          filter: svgFilter,
          transition: 'transform 0.5s ease-in-out',
          // border: '1px solid blue', // For layout debugging
        }}
      >
        <image
          href={pointerAssetUrl}
          x="0"
          y="0"
          width={originalPointerWidth}
          height={originalPointerHeight}
        />
      </svg>
    </div>
  );
}

export default Dial;
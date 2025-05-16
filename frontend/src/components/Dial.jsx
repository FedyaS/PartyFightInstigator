import React from 'react';

function mapValueToAngle(value) {
    // Ensure value is within 0-100 range, as trustLevel is.
    const v = Math.min(100, Math.max(0, value));

    if (v >= 0 && v <= 25) {
      return -2.16 * v + 54;
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

function Dial({ value, svgFilter }) {
  const dialAssetUrl = '/icons/dial.svg';
  const pointerAssetUrl = '/icons/dial-pointer.svg';

  // Overall container size, matching previous .trust-dial-container
  const containerWidth = 120;
  const containerHeight = 120;
  const containerMarginBottom = '2px'; // From original .trust-dial-container

  // Center of the main 120x120 dial container
  const conceptualDialCenterX = containerWidth / 649 * 300;
  const conceptualDialCenterY = containerHeight / 464 * 300;

  // Pointer image dimensions (40% of container, as per original .trust-arrow-svg relative sizing)
  const pointerImgWidth = containerWidth * 0.3;
  const pointerImgHeight = containerHeight * 0.3;

  // The SVG element that will contain and rotate the pointer image.
  // Let this SVG be the size of the pointer image.
  const pointerSvgWidth = pointerImgWidth;
  const pointerSvgHeight = pointerImgHeight;

  // Pivot point for rotation, located at the center of the pointer SVG.
  const pivotX_in_pointerSvg = pointerImgWidth / 200 * 195;
  const pivotY_in_pointerSvg = pointerImgHeight / 84 * 59;

  // Calculate top-left position for the pointer SVG so its pivot aligns with the dial's center.
  const pointerSvgLeft = conceptualDialCenterX - pivotX_in_pointerSvg;
  const pointerSvgTop = conceptualDialCenterY - pivotY_in_pointerSvg;

  const angle = mapValueToAngle(value);
  // The original Dial.jsx used `rotate(${-angle}deg)`.
  const rotationTransform = `rotate(${-angle}deg)`;

  return (
    <div
      style={{
        position: 'relative',
        width: `${containerWidth}px`,
        height: `${containerHeight}px`,
        marginBottom: containerMarginBottom,
        border: '1px dashed grey', // For layout debugging
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
        width={pointerSvgWidth}
        height={pointerSvgHeight}
        viewBox={`0 0 ${pointerSvgWidth} ${pointerSvgHeight}`}
        style={{
          position: 'absolute',
          left: `${pointerSvgLeft}px`,
          top: `${pointerSvgTop}px`,
          transformOrigin: `${pivotX_in_pointerSvg}px ${pivotY_in_pointerSvg}px`,
          transform: rotationTransform,
          filter: svgFilter, // Apply color filter to the pointer as well
          transition: 'transform 0.5s ease-in-out', // Retain transition from original CSS
          border: '1px solid blue', // For layout debugging
        }}
      >
        <image
          href={pointerAssetUrl} // Using href for React compatibility
          x="0"
          y="0"
          width={pointerSvgWidth}    // Pointer image fills its SVG container
          height={pointerSvgHeight}
        />
      </svg>
    </div>
  );
}

export default Dial;
import React from 'react';
import './EmotionBar.css';

function EmotionBar({ angerLevel }) {
  return (
    <div className="emotion-section">
      <div className="anger-label">ANGER</div>
      <div className="emotion-bar">
        <div className="emotion-indicator" style={{ left: `calc(${angerLevel}% - 8px)` }}></div>
      </div>
      <div className="emotion-icons-tray">
        <img src="/icons/happy-face.svg" alt="Happy" className="emotion-icon happy-icon-color" />
        <img src="/icons/neutral-face.svg" alt="Neutral" className="emotion-icon neutral-icon-color" />
        <img src="/icons/angry-face.svg" alt="Angry" className="emotion-icon angry-icon-color" />
      </div>
    </div>
  );
}

export default EmotionBar; 
import React, { useState, useEffect } from 'react';
import './ConversationView.css';
import Dial from './Dial.jsx'; // Explicitly use .jsx and correct casing

function ConversationView() {
  const [npcMessage, setNpcMessage] = useState({ text: 'Hello! I am the CEO. Ask me anything.', isLoading: false });
  const [playerMessage, setPlayerMessage] = useState(null); // Stores the last player message
  const [playerInputText, setPlayerInputText] = useState('');
  const [isPlayerInputLocked, setIsPlayerInputLocked] = useState(false);
  const [angerLevel, setAngerLevel] = useState(50); // Emotion state: 1 (happy) to 100 (angry)
  const [trustLevel, setTrustLevel] = useState(100); // Trust state: 0 (low) to 100 (high)
  const [trustSvgFilter, setTrustSvgFilter] = useState('');

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
    setTrustSvgFilter(calculateFilter());
  }, [trustLevel, P_RED, P_YELLOW, P_GREEN]); // Added dependencies

  const handleSendMessage = () => {
    if (playerInputText.trim() === '' || isPlayerInputLocked) return;

    const newPlayerMessage = { sender: 'player', text: playerInputText };
    setPlayerMessage(newPlayerMessage); // Set only the new message
    setPlayerInputText('');
    setIsPlayerInputLocked(true); // Lock input while NPC "thinks"

    // Simulate NPC response and anger change (example)
    setNpcMessage(prev => ({ ...prev, isLoading: true }));
    setTimeout(() => {
      setNpcMessage({ text: `I received your message: "${newPlayerMessage.text}". That's interesting!`, isLoading: false });
      setIsPlayerInputLocked(false); // Unlock input
      // Example: make NPC slightly angrier after each message for demonstration
      setAngerLevel(prev => Math.min(100, prev + 10));
      // Example: decrease trust slightly after each message
      setTrustLevel(prev => Math.max(0, prev - 5));
    }, 2000);
  };

  // Calculate position for the emotion indicator (1-100 range)
  // If angerLevel is 1, pos is 0%. If angerLevel is 100, pos is 100%.
  const indicatorPositionPercent = angerLevel === 1 ? 0 : (angerLevel - 1) / 99 * 100;

  return (
    <div className="conversation-view-container">
      <div className="npc-area"> {/* Main flex row container for left and right sections */}
        {/* Left Section: NPC Image and Speech Bubble */}
        <div className="npc-info-left">
          <img src="/assets/ceo.png" alt="NPC" className="npc-image" />
          <div className={`speech-bubble npc-speech-bubble ${npcMessage.isLoading ? 'loading' : ''}`}>
            {npcMessage.isLoading ? (
              <div className="loading-dots">
                <span></span><span></span><span></span>
              </div>
            ) : (
              npcMessage.text
            )}
          </div>
        </div>

        {/* Right Section: Trust Meter and Emotion Bar */}
        <div className="npc-indicators-right">
          {/* Trust Meter Section */}
          <div className="trust-meter-section">
            <div className="trust-dial-container"> {/* This class name might be removed from CSS later */}
              <Dial value={trustLevel} svgFilter={trustSvgFilter} />
            </div>
            <div className="trust-label">TRUST</div>
          </div>

          {/* Emotion Bar Section */}
          <div className="emotion-section">
            <div className="anger-label">ANGER</div>
            <div className="emotion-bar">
              <div className="emotion-indicator" style={{ left: `calc(${indicatorPositionPercent}% - 6px)` }}></div>
            </div>
            <div className="emotion-icons-tray">
              <img src="/icons/happy-face.svg" alt="Happy" className="emotion-icon happy-icon-color" />
              <img src="/icons/neutral-face.svg" alt="Neutral" className="emotion-icon neutral-icon-color" />
              <img src="/icons/angry-face.svg" alt="Angry" className="emotion-icon angry-icon-color" />
            </div>
          </div>
        </div>
      </div>

      <div className="chat-log">
        {playerMessage && (
          <div className={`speech-bubble player-speech-bubble`}>
            {playerMessage.text}
          </div>
        )}
      </div>

      <div className="input-area">
        <div className={`input-wrapper ${isPlayerInputLocked ? 'locked' : ''}`}>
          <input
            type="text"
            value={playerInputText}
            onChange={(e) => setPlayerInputText(e.target.value)}
            placeholder={isPlayerInputLocked ? '' : 'Type your message...'}
            disabled={isPlayerInputLocked}
            className="chat-input"
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          {isPlayerInputLocked && <img src="/icons/lock.svg" alt="Locked" className="lock-icon" />}
        </div>
        <button onClick={handleSendMessage} disabled={isPlayerInputLocked} className="send-button">
          <img src="/icons/send.svg" alt="Send" />
        </button>
      </div>
    </div>
  );
}

export default ConversationView; 
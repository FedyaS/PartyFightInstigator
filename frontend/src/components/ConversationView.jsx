import React, { useState, useEffect } from 'react';
import './ConversationView.css';
import Dial from './Dial.jsx'; // Explicitly use .jsx and correct casing

function ConversationView() {
  const [npcMessage, setNpcMessage] = useState({ text: 'Hello! I am the CEO. Ask me anything.', isLoading: false });
  const [playerMessage, setPlayerMessage] = useState(null); // Stores the last player message
  const [playerInputText, setPlayerInputText] = useState('');
  const [isPlayerInputLocked, setIsPlayerInputLocked] = useState(false);
  const [angerLevel, setAngerLevel] = useState(100); // Emotion state: 1 (happy) to 100 (angry)
  const [trustLevel, setTrustLevel] = useState(25); // Trust state: 0 (low) to 100 (high)

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
              <Dial trustLevel={trustLevel} />
            </div>
            <div className="trust-label">TRUST</div>
          </div>

          {/* Emotion Bar Section */}
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
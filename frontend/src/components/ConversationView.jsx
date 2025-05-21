import React, { useState, useEffect, useRef } from 'react';
import './ConversationView.css';
import Dial from './Dial.jsx';
import EmotionBar from './EmotionBar.jsx';

function ConversationView() {
  const inputRef = useRef(null);
  const [npcMessage, setNpcMessage] = useState({ text: 'Hello! I am the CEO. Ask me anything.', isLoading: false });
  const [playerMessage, setPlayerMessage] = useState(null);
  const [playerInputText, setPlayerInputText] = useState('');
  const [isPlayerInputLocked, setIsPlayerInputLocked] = useState(false);
  const [angerLevel, setAngerLevel] = useState(57);
  const [trustLevel, setTrustLevel] = useState(25);

  useEffect(() => {
    if (!isPlayerInputLocked) {
      // Small delay to ensure the input is enabled before focusing
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  }, [isPlayerInputLocked]);

  const handleSendMessage = () => {
    if (playerInputText.trim() === '' || isPlayerInputLocked) return;

    const newPlayerMessage = { sender: 'player', text: playerInputText };
    setPlayerMessage(newPlayerMessage);
    setPlayerInputText('');
    setIsPlayerInputLocked(true);

    setNpcMessage(prev => ({ ...prev, isLoading: true }));
    setTimeout(() => {
      setNpcMessage({ text: `I received your message: "${newPlayerMessage.text}". That's interesting!`, isLoading: false });
      setIsPlayerInputLocked(false);
      setAngerLevel(prev => Math.min(100, prev + 10));
      setTrustLevel(prev => Math.max(0, prev - 5));
    }, 2000);
  };

  return (
    <div className="conversation-view-container">
      <div className="main-content">
        {/* Left Section */}
        <div className="left-section">
          {/* Top: NPC Image and Message */}
          <div className="npc-info-top">
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

          {/* Bottom: Chat Log */}
          <div className="chat-log">
            {playerMessage && (
              <div className={`speech-bubble player-speech-bubble`}>
                {playerMessage.text}
              </div>
            )}
          </div>
        </div>

        {/* Right Section: Indicators */}
        <div className="npc-indicators-right">
          <div className="trust-meter-section">
            <Dial trustLevel={trustLevel} />
            <div className="trust-label">TRUST</div>
          </div>
          <div className='anger-bar-section'>
            <EmotionBar angerLevel={angerLevel} />
          </div>
        </div>
      </div>

      <div className="input-area">
        <div className={`input-wrapper ${isPlayerInputLocked ? 'locked' : ''}`}>
          <input
            ref={inputRef}
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
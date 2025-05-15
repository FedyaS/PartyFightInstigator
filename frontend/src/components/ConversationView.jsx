import React, { useState, useEffect } from 'react';
import './ConversationView.css';

function ConversationView() {
  const [npcMessage, setNpcMessage] = useState({ text: 'Hello! I am the CEO. Ask me anything.', isLoading: false });
  const [playerMessages, setPlayerMessages] = useState([]); // Stores a list of player messages
  const [playerInputText, setPlayerInputText] = useState('');
  const [isPlayerInputLocked, setIsPlayerInputLocked] = useState(false);

  const handleSendMessage = () => {
    if (playerInputText.trim() === '' || isPlayerInputLocked) return;

    const newPlayerMessage = { sender: 'player', text: playerInputText };
    setPlayerMessages(prevMessages => [...prevMessages, newPlayerMessage]);
    setPlayerInputText('');
    setIsPlayerInputLocked(true); // Lock input while NPC "thinks"

    // Simulate NPC response
    setNpcMessage(prev => ({ ...prev, isLoading: true }));
    setTimeout(() => {
      setNpcMessage({ text: `I received your message: "${newPlayerMessage.text}". That's interesting!`, isLoading: false });
      setIsPlayerInputLocked(false); // Unlock input
    }, 2000);
  };

  return (
    <div className="conversation-view-container">
      <div className="npc-area">
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

      <div className="chat-log">
        {playerMessages.map((msg, index) => (
          <div key={index} className={`speech-bubble player-speech-bubble`}>
            {msg.text}
          </div>
        ))}
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
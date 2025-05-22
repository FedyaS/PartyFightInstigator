import React from 'react';
import './NPCCard.css';

function NPCCard({ npc, onFriendClick, onFoeClick, onNext, onPrev }) {
  return (
    <div className="npc-card">
      <div className="npc-header">
        <div className="npc-header-content">
          <div className="npc-card-image-container">
            <img src={npc.image} alt={npc.name} className="npc-card-image" />
          </div>
          <h3 className="npc-card-name">{npc.name}</h3>
        </div>
      </div>
      
      <div className="npc-card-stats">
        <div className="card-stat">
          <span className="card-stat-label">Trust</span>
          <span className="card-stat-value">{npc.trust}</span>
        </div>
        <div className="card-stat">
          <span className="card-stat-label">Anger</span>
          <span className="card-stat-value">{npc.anger}</span>
        </div>
        <div className="card-stat">
          <span className="card-stat-label">Stat3</span>
          <span className="card-stat-value">{npc.stat3}</span>
        </div>
        <div className="card-stat">
          <span className="card-stat-label">Stat4</span>
          <span className="card-stat-value">{npc.stat4}</span>
        </div>
      </div>

      <div className="npc-card-description">
        <p>{npc.description}</p>
      </div>

      <div className="npc-card-relationships">
        <div className="friends">
          <h4>Friends</h4>
          <ul>
            {[...Array(4)].map((_, index) => (
              <li 
                key={index} 
                onClick={() => npc.friends[index] && onFriendClick(npc.friends[index].id)}
                className={!npc.friends[index] ? 'empty-slot' : ''}
              >
                {npc.friends[index] ? npc.friends[index].name : '—'}
              </li>
            ))}
          </ul>
        </div>
        <div className="foes">
          <h4>Foes</h4>
          <ul>
            {[...Array(4)].map((_, index) => (
              <li 
                key={index} 
                onClick={() => npc.foes[index] && onFoeClick(npc.foes[index].id)}
                className={!npc.foes[index] ? 'empty-slot' : ''}
              >
                {npc.foes[index] ? npc.foes[index].name : '—'}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="npc-card-navigation">
        <button onClick={onPrev} className="nav-button">←</button>
        <button onClick={onNext} className="nav-button">→</button>
      </div>
    </div>
  );
}

export default NPCCard; 
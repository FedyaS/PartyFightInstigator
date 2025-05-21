import React, { useState } from 'react';
import './PlayerNotes.css';

function PlayerNotes() {
  const [notes, setNotes] = useState('');

  return (
    <div className="player-notes-container">
      <div className="player-notes-label">NOTES</div>
      <textarea
        className="player-notes-input"
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        placeholder="Take notes..."
      />
    </div>
  );
}

export default PlayerNotes; 
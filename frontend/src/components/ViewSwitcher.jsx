import React from 'react';
import './ViewSwitcher.css';

function ViewSwitcher({ activeView, onViewChange }) {
  return (
    <div className="view-switcher">
      <button 
        className={`view-option ${activeView === 'MAP' ? 'active' : ''}`}
        onClick={() => onViewChange('MAP')}
      >
        MAP
      </button>
      <button 
        className={`view-option ${activeView === 'ATTENDEES' ? 'active' : ''}`}
        onClick={() => onViewChange('ATTENDEES')}
      >
        ATTENDEES
      </button>
    </div>
  );
}

export default ViewSwitcher; 
import GameStats from './GameStats';
import ConversationView from './ConversationView';
import ViewSwitcher from './ViewSwitcher';
import AttendeesView from './AttendeesView';
import './GameLayout.css';
import { useState } from 'react';

function GameLayout({ children }) {
  const [activeView, setActiveView] = useState('MAP');

  return (
    <div className="layout-container">
      <div className="status-bar">
        {/* <h2 className="status-title">Status</h2> */}
        <GameStats /> {/* Added GameStats component */}
      </div>
      <div className="layout-main">
        <ConversationView /> {/* Added ConversationView component */}
        <aside className="graph-section">
          <ViewSwitcher activeView={activeView} onViewChange={setActiveView} />
          {activeView === 'MAP' ? (
            <div className="map-view">
              <img src="/mapBG1.png" alt="Map Background" className="map-background" />
            </div>
          ) : (
            <AttendeesView />
          )}
        </aside>
      </div>
    </div>
  );
}

export default GameLayout;
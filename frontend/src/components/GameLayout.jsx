import GameStats from './GameStats';
import CharacterAnimation from './CharacterAnimation';

function GameLayout({ children }) {
  return (
    <div className="layout-container">
      <div className="status-bar">
        <GameStats />
      </div>
      <div className="layout-main">
        <aside className="sidebar">
          <h3 className="sidebar-title">Chats / NPC Info</h3>
          <p>Chat messages or NPC details will appear here</p>
        </aside>
        <main className="content-area">
          {children}
          <div className="svg-placeholder">
            <CharacterAnimation dialogue="Hello, party crasher!" />
          </div>
        </main>
        <aside className="graph-section">
          <h3 className="graph-title">Graph</h3>
          <p>Graph placeholder (to be implemented)</p>
        </aside>
      </div>
    </div>
  );
}

export default GameLayout;
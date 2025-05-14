import GameStats from './GameStats';
import './GameLayout.css';

function GameLayout({ children }) {
  return (
    <div className="layout-container">
      <div className="status-bar">
        {/* <h2 className="status-title">Status</h2> */}
        <GameStats /> {/* Added GameStats component */}
      </div>
      <div className="layout-main">
        <aside className="sidebar">
          <h3 className="sidebar-title">Chats / NPC Info</h3>
          <p>Chat messages or NPC details will appear here</p>
        </aside>
        <main className="content-area">
          {children}
          <div className="svg-placeholder">SVG or Game Content Here</div>
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
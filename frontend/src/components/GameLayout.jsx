import GameStats from './GameStats';
import ConversationView from './ConversationView';
import './GameLayout.css';

function GameLayout({ children }) {
  return (
    <div className="layout-container">
      <div className="status-bar">
        {/* <h2 className="status-title">Status</h2> */}
        <GameStats /> {/* Added GameStats component */}
      </div>
      <div className="layout-main">
        <main className="content-area">
          <ConversationView /> {/* Added ConversationView component */}
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
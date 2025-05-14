import { useNavigate } from 'react-router-dom';
import './MainStats.css';

const MainStats = () => {
  const navigate = useNavigate();
  
  // These would typically come from a state management system or API
  const userStats = {
    username: "Player1",
    levelsPassed: 0,
    timePlayed: "0h 0m"
  };

  const handleStartGame = () => {
    navigate('/game');
  };

  return (
    <div className="main-stats">
      <div className="stats-container">
        <h2>Player Stats</h2>
        <div className="stat-item">
          <span className="stat-label">Username:</span>
          <span className="stat-value">{userStats.username}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Levels Passed:</span>
          <span className="stat-value">{userStats.levelsPassed}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Time Played:</span>
          <span className="stat-value">{userStats.timePlayed}</span>
        </div>
        <button 
          className="start-button"
          onClick={handleStartGame}
        >
          Start Game
        </button>
      </div>
    </div>
  );
};

export default MainStats; 
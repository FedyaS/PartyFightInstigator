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
          <div className="stat-icon">
            <img src="/icons/user-icon.svg" alt="User Icon" width="30" height="30" />
          </div>
          <div className="stat-info">
            <span className="stat-value">{userStats.username}</span>
            <span className="stat-label">Username</span>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">
            <img src="/icons/level-icon.svg" alt="Level Icon" width="30" height="30" />
          </div>
          <div className="stat-info">
            <span className="stat-value">{userStats.levelsPassed}</span>
            <span className="stat-label">Levels Passed</span>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">
            <img src="/icons/time-icon.svg" alt="Time Icon" width="30" height="30" />
          </div>
          <div className="stat-info">
            <span className="stat-value">{userStats.timePlayed}</span>
            <span className="stat-label">Time Played</span>
          </div>
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
import { useState, useEffect } from 'react';

function GameStats() {
  const gameState = {
    level_name: "1",
    user_name: "PartyCrasher17",
    time_started: "2025-04-25T05:44:55Z",
    chaos_meter: 67,
    party_headcount: 13,
    personal_risk: 50,
    active_rumors: 3,
    goal: "Push chaos above 95"
  };

  // Calculate elapsed time
  const startTime = new Date(gameState.time_started).getTime();
  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      const elapsedSeconds = Math.floor((now - startTime) / 1000);
      setElapsedTime(Math.max(0, elapsedSeconds));
    }, 1000);

    return () => clearInterval(interval);
  }, [startTime]);

  const minutes = Math.floor(elapsedTime / 60).toString().padStart(2, '0');
  const seconds = (elapsedTime % 60).toString().padStart(2, '0');

  return (
    <div className="game-stats">
      <div className="stats-grid">
        {/* Row 1: User, Chaos Meter, Personal Risk, Goal */}
        <div className="stat-item">
          <div className="stat-icon">
            <img src="/icons/user-icon.svg" alt="User Icon" width="40" height="40" />
          </div>
          <div className="stat-info">
            <span className="stat-value">{gameState.user_name}</span>
            <span className="stat-label">User</span>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">
            <img src="/icons/chaos-icon.svg" alt="Chaos Icon" width="40" height="40" />
          </div>
          <div className="stat-info">
            <span className="stat-value">{gameState.chaos_meter}</span>
            <span className="stat-label">Chaos Meter</span>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">
            <img src="/icons/risk-icon.svg" alt="Risk Icon" width="40" height="40" />
          </div>
          <div className="stat-info">
            <span className="stat-value">{gameState.personal_risk}</span>
            <span className="stat-label">Personal Risk</span>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">
            <img src="/icons/goal-icon.svg" alt="Goal Icon" width="40" height="40" />
          </div>
          <div className="stat-info">
            <span className="stat-value">{gameState.goal}</span>
            <span className="stat-label">Goal</span>
          </div>
        </div>

        {/* Row 2: Level, Party Headcount, Active Rumors, Time Elapsed */}
        <div className="stat-item">
          <div className="stat-icon">
            <img src="/icons/level-icon.svg" alt="Level Icon" width="40" height="40" />
          </div>
          <div className="stat-info">
            <span className="stat-value">{gameState.level_name}</span>
            <span className="stat-label">Level</span>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">
            <img src="/icons/headcount-icon.svg" alt="Headcount Icon" width="40" height="40" />
          </div>
          <div className="stat-info">
            <span className="stat-value">{gameState.party_headcount}</span>
            <span className="stat-label">Party Headcount</span>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">
            <img src="/icons/rumors-icon.svg" alt="Rumors Icon" width="40" height="40" />
          </div>
          <div className="stat-info">
            <span className="stat-value">{gameState.active_rumors}</span>
            <span className="stat-label">Active Rumors</span>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">
            <img src="/icons/time-icon.svg" alt="Time Icon" width="40" height="40" />
          </div>
          <div className="stat-info">
            <span className="stat-value">{minutes}:{seconds}</span>
          </div>
        </div>
      </div>
    </div>
  );
}


export default GameStats;

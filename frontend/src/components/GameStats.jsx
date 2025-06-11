import { useState, useEffect } from "react";
import { useSelector } from "react-redux";

function GameStats() {
	const user_name = "PartyCrasher17";
	const {
		level,
		time_started,
		chaos_meter,
		party_headcount,
		personal_risk,
		active_rumors,
		goal,
	} = useSelector((state) => state.game);

	// Calculate elapsed time
	const startTime = new Date(time_started).getTime();
	const [elapsedTime, setElapsedTime] = useState(0);

	useEffect(() => {
		const interval = setInterval(() => {
			const now = Date.now();
			const elapsedSeconds = Math.floor((now - startTime) / 1000);
			setElapsedTime(Math.max(0, elapsedSeconds));
		}, 1000);

		return () => clearInterval(interval);
	}, [startTime]);

	const minutes = Math.floor(elapsedTime / 60)
		.toString()
		.padStart(2, "0");
	const seconds = (elapsedTime % 60).toString().padStart(2, "0");

	return (
		<div className="game-stats">
			<div className="stats-grid">
				{/* Row 1: User, Chaos Meter, Personal Risk, Goal */}
				<div className="stat-item">
					<div className="stat-icon">
						<img
							src="/icons/user-icon.svg"
							alt="User Icon"
							width="40"
							height="40"
						/>
					</div>
					<div className="stat-info">
						<span className="stat-value">{user_name}</span>
						<span className="stat-label">User</span>
					</div>
				</div>
				<div className="stat-item">
					<div className="stat-icon">
						<img
							src="/icons/chaos-icon.svg"
							alt="Chaos Icon"
							width="40"
							height="40"
						/>
					</div>
					<div className="stat-info">
						<span className="stat-value">{chaos_meter}</span>
						<span className="stat-label">Chaos Meter</span>
					</div>
				</div>
				<div className="stat-item">
					<div className="stat-icon">
						<img
							src="/icons/risk-icon.svg"
							alt="Risk Icon"
							width="40"
							height="40"
						/>
					</div>
					<div className="stat-info">
						<span className="stat-value">{personal_risk}</span>
						<span className="stat-label">Personal Risk</span>
					</div>
				</div>
				<div className="stat-item">
					<div className="stat-icon">
						<img
							src="/icons/goal-icon.svg"
							alt="Goal Icon"
							width="40"
							height="40"
						/>
					</div>
					<div className="stat-info">
						<span className="stat-value">{goal}</span>
						<span className="stat-label">Goal</span>
					</div>
				</div>

				{/* Row 2: Level, Party Headcount, Active Rumors, Time Elapsed */}
				<div className="stat-item">
					<div className="stat-icon">
						<img
							src="/icons/level-icon.svg"
							alt="Level Icon"
							width="40"
							height="40"
						/>
					</div>
					<div className="stat-info">
						<span className="stat-value">{level}</span>
						<span className="stat-label">Level</span>
					</div>
				</div>
				<div className="stat-item">
					<div className="stat-icon">
						<img
							src="/icons/headcount-icon.svg"
							alt="Headcount Icon"
							width="40"
							height="40"
						/>
					</div>
					<div className="stat-info">
						<span className="stat-value">{party_headcount}</span>
						<span className="stat-label">Party Headcount</span>
					</div>
				</div>
				<div className="stat-item">
					<div className="stat-icon">
						<img
							src="/icons/rumors-icon.svg"
							alt="Rumors Icon"
							width="40"
							height="40"
						/>
					</div>
					<div className="stat-info">
						<span className="stat-value">{active_rumors}</span>
						<span className="stat-label">Active Rumors</span>
					</div>
				</div>
				<div className="stat-item">
					<div className="stat-icon">
						<img
							src="/icons/time-icon.svg"
							alt="Time Icon"
							width="40"
							height="40"
						/>
					</div>
					<div className="stat-info">
						<span className="stat-value">
							{minutes}:{seconds}
						</span>
					</div>
				</div>
			</div>
		</div>
	);
}

export default GameStats;

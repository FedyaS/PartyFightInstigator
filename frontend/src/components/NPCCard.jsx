import React from "react";
import "./NPCCard.css";

function NPCCard({ npc, onNext, onPrev }) {
	// Handle case where npc might be undefined
	if (!npc) {
		return <div className="npc-card">Loading...</div>;
	}

	return (
		<div className="npc-card">
			<div className="npc-header">
				<div className="npc-header-content">
					<div className="npc-card-image-container">
						<img
							src={`/assets/${npc.id}.png`}
							alt={npc.name}
							className="npc-card-image"
						/>
					</div>
					<h3 className="npc-card-name">{npc.name}</h3>
				</div>
			</div>

			<div className="npc-card-stats">
				<div className="card-stat">
					<span className="card-stat-label">Relationship</span>
					<span className="card-stat-value">{npc.relationship_score}</span>
				</div>
				<div className="card-stat">
					<span className="card-stat-label">Anger</span>
					<span className="card-stat-value">{npc.anger}</span>
				</div>
				<div className="card-stat">
					<span className="card-stat-label">Gullibility</span>
					<span className="card-stat-value">{npc.gullibility}</span>
				</div>
				<div className="card-stat">
					<span className="card-stat-label">Personality</span>
					<span className="card-stat-value">{npc.personality}</span>
				</div>
			</div>

			<div className="npc-card-navigation">
				<button onClick={onPrev} className="nav-button">
					←
				</button>
				<button onClick={onNext} className="nav-button">
					→
				</button>
			</div>
		</div>
	);
}

export default NPCCard;

import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import "./NPCCard.css";

function NPCCard({ npc, onNext, onPrev, setActiveNpcId, onNavigateToNPC }) {
	const npcs = useSelector((state) => state.game.npcs);
	const npcConversations = useSelector((state) => state.game.npcConversations);

	const [dots, setDots] = useState("...");

	// Animated dots effect
	useEffect(() => {
		const interval = setInterval(() => {
			setDots((prev) => (prev.length >= 3 ? "." : prev + "."));
		}, 500);
		return () => clearInterval(interval);
	}, []);

	// Handle case where npc might be undefined
	if (!npc) {
		return <div className="npc-card">Loading...</div>;
	}

	const handleTalkToNPC = () => {
		setActiveNpcId(npc.id);
	};

	const renderConversationStatus = () => {
		if (!npc.conversation_id) {
			return `${npc.name} is not talking to anybody`;
		}

		const conversation = npcConversations[npc.conversation_id];
		if (!conversation) {
			return `${npc.name} is not talking to anybody`;
		}

		const otherParticipants = conversation.participants.filter(
			(id) => id !== npc.id
		);
		if (otherParticipants.length === 0) {
			return `${npc.name} is not talking to anybody`;
		}

		const participantNames = otherParticipants.map((id) => {
			const participantNpc = npcs[id];
			return participantNpc ? participantNpc.name : id;
		});

		return (
			<span>
				{npc.name} is currently talking with{" "}
				{participantNames.map((name, index) => (
					<span key={index}>
						<span
							className="conversation-participant"
							onClick={() => onNavigateToNPC(otherParticipants[index])}
						>
							{name}
						</span>
						{index < participantNames.length - 1 ? ", " : ""}
					</span>
				))}
				{dots}
			</span>
		);
	};

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
					<button className="talk-to-npc-button" onClick={handleTalkToNPC}>
						TALK TO NPC
					</button>
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

			<div className="npc-conversation-status">
				<div className="conversation-label">Active Conversation:</div>
				<div className="conversation-text">{renderConversationStatus()}</div>
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

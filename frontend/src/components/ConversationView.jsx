import React, { useState, useEffect, useRef } from "react";
import { useSelector, useDispatch } from "react-redux";
import {
	sendPlayerMessage,
	updatePlayerConversation,
} from "../store/gameSlice";
import "./ConversationView.css";
import Dial from "./Dial.jsx";
import EmotionBar from "./EmotionBar.jsx";
import VoiceDotCone from "./VoiceDotCone.jsx";
import PlayerNotes from "./PlayerNotes.jsx";

function ConversationView({ activeNpcId }) {
	const inputRef = useRef(null);
	const dispatch = useDispatch();
	const activeNpc = useSelector((state) => state.game.npcs[activeNpcId]);

	const [playerInputText, setPlayerInputText] = useState("");
	const [animationDirection, setAnimationDirection] = useState("none");
	const [isPlayerInputLocked, setIsPlayerInputLocked] = useState(false);

	// Derived values from Redux:
	const npcMessage = {
		text: activeNpc?.playerConversation.last_npc_message || "",
		isLoading: activeNpc?.playerConversation.NPC_is_thinking || false,
	};
	const playerMessage = activeNpc?.playerConversation.last_player_message
		? { text: activeNpc.playerConversation.last_player_message }
		: null;
	const angerLevel = activeNpc?.anger || 0;
	const trustLevel = activeNpc?.relationship_score || 0;

	useEffect(() => {
		if (!isPlayerInputLocked) {
			// Small delay to ensure the input is enabled before focusing
			setTimeout(() => {
				inputRef.current?.focus();
			}, 100);
		}
	}, [isPlayerInputLocked]);

	const handleSendMessage = () => {
		if (playerInputText.trim() === "" || isPlayerInputLocked) return;

		setPlayerInputText("");
		setIsPlayerInputLocked(true);
		setAnimationDirection("up");

		dispatch(
			sendPlayerMessage({
				npcId: activeNpcId,
				message: playerInputText,
			})
		);

		// Mock response (replace with real backend call later)
		setTimeout(() => {
			dispatch(
				updatePlayerConversation({
					npcId: activeNpcId,
					last_npc_message: `I received: "${playerInputText}". Interesting!`,
					last_message_is: "NPC",
					NPC_is_thinking: false,
				})
			);
			setIsPlayerInputLocked(false);
			setAnimationDirection("down");
		}, 2000);
	};

	return (
		<div className="conversation-view-container">
			<div className="main-content">
				{/* Left Section */}
				<div className="left-section">
					{/* Top: NPC Image and Message */}
					<div className="npc-info-top">
						<img
							src={`/assets/${activeNpcId}.png`}
							alt="NPC"
							className="npc-image"
						/>
						<div
							className={`speech-bubble npc-speech-bubble ${
								npcMessage.isLoading ? "loading" : ""
							}`}
						>
							{npcMessage.isLoading ? (
								<div className="loading-dots">
									<span></span>
									<span></span>
									<span></span>
								</div>
							) : (
								npcMessage.text
							)}
						</div>
					</div>

					<div className="dot-pattern-container">
						{/* <DotPattern size={150} animationDirection="down" /> */}
						<VoiceDotCone
							size={150}
							animationDirection={animationDirection}
							animationCycles={1}
							color="rgba(0, 50, 70, 0.9)"
						/>
					</div>

					{/* Bottom: Player Image and Message */}
					<div className="player-info-bottom">
						<div className={`speech-bubble player-speech-bubble`}>
							{playerMessage?.text}
						</div>
						<img src="/assets/elon.png" alt="Player" className="player-image" />
					</div>
				</div>

				{/* Right Section: Indicators */}
				<div className="npc-indicators-right">
					<div className="trust-meter-section">
						<Dial trustLevel={trustLevel} />
						<div className="trust-label">TRUST</div>
					</div>
					<div className="anger-bar-section">
						<EmotionBar angerLevel={angerLevel} />
					</div>
					<PlayerNotes />
				</div>
			</div>

			<div className="input-area">
				<div className={`input-wrapper ${isPlayerInputLocked ? "locked" : ""}`}>
					<input
						ref={inputRef}
						type="text"
						value={playerInputText}
						onChange={(e) => setPlayerInputText(e.target.value)}
						placeholder={isPlayerInputLocked ? "" : "Type your message..."}
						disabled={isPlayerInputLocked}
						className="chat-input"
						onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
					/>
					{isPlayerInputLocked && (
						<img src="/icons/lock.svg" alt="Locked" className="lock-icon" />
					)}
				</div>
				<button
					onClick={handleSendMessage}
					disabled={isPlayerInputLocked}
					className="send-button"
				>
					<img src="/icons/send.svg" alt="Send" />
				</button>
			</div>
		</div>
	);
}

export default ConversationView;

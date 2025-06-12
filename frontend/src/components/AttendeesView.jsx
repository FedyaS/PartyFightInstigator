import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import NPCCard from "./NPCCard";
import "./AttendeesView.css";

function AttendeesView() {
	const npcs = useSelector((state) => state.game.npcs);
	const npcArray = Object.values(npcs);

	const [currentNPCIndex, setCurrentNPCIndex] = useState(0);
	const [currentNPC, setCurrentNPC] = useState(npcArray[0]);

	useEffect(() => {
		setCurrentNPC(npcArray[currentNPCIndex]);
	}, [currentNPCIndex, npcArray]);

	const handleNext = () => {
		setCurrentNPCIndex((prev) => (prev + 1) % npcArray.length);
	};

	const handlePrev = () => {
		setCurrentNPCIndex(
			(prev) => (prev - 1 + npcArray.length) % npcArray.length
		);
	};

	// Add keyboard navigation
	useEffect(() => {
		const handleKeyPress = (e) => {
			if (e.key === "ArrowLeft") {
				handlePrev();
			} else if (e.key === "ArrowRight") {
				handleNext();
			}
		};

		window.addEventListener("keydown", handleKeyPress);
		return () => window.removeEventListener("keydown", handleKeyPress);
	}, []);

	return (
		<div className="attendees-view">
			<NPCCard npc={currentNPC} onNext={handleNext} onPrev={handlePrev} />
		</div>
	);
}

export default AttendeesView;

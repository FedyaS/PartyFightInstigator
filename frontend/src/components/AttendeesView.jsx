import React, { useState, useEffect } from 'react';
import NPCCard from './NPCCard';
import './AttendeesView.css';

// Sample NPC data - replace with actual data later
const sampleNPCs = [
  {
    id: 1,
    name: "CEO",
    image: "/assets/ceo.png",
    trust: 75,
    anger: 20,
    stat3: 85,
    stat4: 60,
    description: "The charismatic leader of the company. Known for bold decisions and a sharp mind.",
    friends: [
      { id: 2, name: "Elon" },
      { id: 3, name: "Sarah" }
    ],
    foes: [
      { id: 4, name: "Mark" }
    ]
  },
  {
    id: 2,
    name: "Elon",
    image: "/assets/elon.png",
    trust: 65,
    anger: 35,
    stat3: 90,
    stat4: 70,
    description: "Innovative thinker with a controversial reputation. Always pushing boundaries.",
    friends: [
      { id: 1, name: "CEO" }
    ],
    foes: [
      { id: 4, name: "Mark" }
    ]
  }
];

function AttendeesView() {
  const [currentNPCIndex, setCurrentNPCIndex] = useState(0);
  const [currentNPC, setCurrentNPC] = useState(sampleNPCs[0]);

  useEffect(() => {
    setCurrentNPC(sampleNPCs[currentNPCIndex]);
  }, [currentNPCIndex]);

  const handleNext = () => {
    setCurrentNPCIndex((prev) => (prev + 1) % sampleNPCs.length);
  };

  const handlePrev = () => {
    setCurrentNPCIndex((prev) => (prev - 1 + sampleNPCs.length) % sampleNPCs.length);
  };

  const handleFriendClick = (friendId) => {
    const friendIndex = sampleNPCs.findIndex(npc => npc.id === friendId);
    if (friendIndex !== -1) {
      setCurrentNPCIndex(friendIndex);
    }
  };

  const handleFoeClick = (foeId) => {
    const foeIndex = sampleNPCs.findIndex(npc => npc.id === foeId);
    if (foeIndex !== -1) {
      setCurrentNPCIndex(foeIndex);
    }
  };

  // Add keyboard navigation
  useEffect(() => {
    const handleKeyPress = (e) => {
      if (e.key === 'ArrowLeft') {
        handlePrev();
      } else if (e.key === 'ArrowRight') {
        handleNext();
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, []);

  return (
    <div className="attendees-view">
      <NPCCard
        npc={currentNPC}
        onFriendClick={handleFriendClick}
        onFoeClick={handleFoeClick}
        onNext={handleNext}
        onPrev={handlePrev}
      />
    </div>
  );
}

export default AttendeesView; 
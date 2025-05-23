import { useEffect, useState } from 'react';
import './NPCOnMap.css';

function NPCOnMap({ image, initialX, initialY, maxX, maxY }) {
  const [position, setPosition] = useState({ x: initialX, y: initialY });
  const [isMoving, setIsMoving] = useState(true);

  useEffect(() => {
    const moveInterval = setInterval(() => {
      if (isMoving) {
        // Random movement
        const directions = [
          { x: 0, y: -1 },  // up
          { x: 0, y: 1 },   // down
          { x: -1, y: 0 },  // left
          { x: 1, y: 0 },   // right
          { x: -1, y: -1 }, // diagonal up-left
          { x: 1, y: -1 },  // diagonal up-right
          { x: -1, y: 1 },  // diagonal down-left
          { x: 1, y: 1 },   // diagonal down-right
        ];
        
        const randomDirection = directions[Math.floor(Math.random() * directions.length)];
        const newX = Math.max(0, Math.min(maxX, position.x + randomDirection.x * 5));
        const newY = Math.max(0, Math.min(maxY, position.y + randomDirection.y * 5));
        
        setPosition({ x: newX, y: newY });
      }
    }, 100);

    // Randomly stop and start moving
    const movementInterval = setInterval(() => {
      setIsMoving(prev => !prev);
    }, Math.random() * 3000 + 2000); // Random time between 2-5 seconds

    return () => {
      clearInterval(moveInterval);
      clearInterval(movementInterval);
    };
  }, [position, isMoving, maxX, maxY]);

  return (
    <div 
      className="npc-on-map"
      style={{
        left: `${position.x}px`,
        top: `${position.y}px`,
      }}
    >
      <img src={image} alt="NPC" />
    </div>
  );
}

export default NPCOnMap; 
import { useState, useRef, useEffect } from 'react';
import NPCOnMap from './NPCOnMap';
import './MapView.css';

function MapView() {
  const mapRef = useRef(null);
  const [mapDimensions, setMapDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    const updateDimensions = () => {
      if (mapRef.current) {
        setMapDimensions({
          width: mapRef.current.offsetWidth,
          height: mapRef.current.offsetHeight
        });
      }
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  const [npcs] = useState([
    { id: 1, image: "/assets/ceo.png", initialX: 100, initialY: 100 },
    { id: 2, image: "/assets/elon.png", initialX: 200, initialY: 200 },
  ]);

  return (
    <div className="map-view" ref={mapRef}>
      <img src="/mapBG1.png" alt="Map Background" className="map-background" />
      <div className="npcs-container">
        {npcs.map(npc => (
          <NPCOnMap
            key={npc.id}
            image={npc.image}
            initialX={npc.initialX}
            initialY={npc.initialY}
            maxX={mapDimensions.width - 40} // Subtract NPC width
            maxY={mapDimensions.height - 40} // Subtract NPC height
          />
        ))}
      </div>
    </div>
  );
}

export default MapView; 
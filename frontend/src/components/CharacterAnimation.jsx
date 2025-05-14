import { useRef } from 'react';
import { Canvas, useFrame, useLoader } from '@react-three/fiber';
import { TextureLoader } from 'three';
import { Text } from '@react-three/drei';

function CharacterScene({ dialogue }) {
  const characterRef = useRef();
  const bubbleRef = useRef();
  let characterTexture, bubbleTexture;

    characterTexture = useLoader(TextureLoader, '/assets/character.png');
    bubbleTexture = useLoader(TextureLoader, '/assets/bubble.png');

  useFrame(({ clock }) => {
    if (characterRef.current) {
      characterRef.current.position.y = Math.sin(clock.getElapsedTime()) * 0.1;
    }
    if (bubbleRef.current) {
      bubbleRef.current.scale.set(
        1 + Math.sin(clock.getElapsedTime()) * 0.05,
        1 + Math.sin(clock.getElapsedTime()) * 0.05,
        1
      );
    }
  });

  return (
    <>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <mesh ref={characterRef} position={[0, -0.5, 0]}>
        <planeGeometry args={[1, 1]} />
        <meshBasicMaterial
          map={characterTexture}
          transparent
          color={characterTexture ? undefined : 'red'}
        />
      </mesh>
      <mesh ref={bubbleRef} position={[0, 0.7, 0]}>
        <planeGeometry args={[1.5, 0.5]} />
        <meshBasicMaterial
          map={bubbleTexture}
          transparent
          color={bubbleTexture ? undefined : 'white'}
        />
      </mesh>
      <Text
        position={[0, 0.7, 0.1]}
        fontSize={0.15}
        color="black"
        anchorX="center"
        anchorY="middle"
        maxWidth={1.2}
        lineHeight={1.2}
      >
        {dialogue}
      </Text>
      {/* Adjusted background size */}
      <mesh position={[0, 0, -2]}>
        <planeGeometry args={[5, 5]} /> {/* Smaller size */}
        <meshBasicMaterial color="#4a235a" />
      </mesh>
    </>
  );
}

function CharacterAnimation({ dialogue = 'Let’s cause some chaos!' }) {
  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <Canvas
        camera={{ position: [0, 0, 5], fov: 50 }}
        style={{ background: 'transparent' }} // Ensure canvas background is transparent
        onCreated={({ gl }) => {
          gl.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        }}
      >
        <CharacterScene dialogue={dialogue} />
      </Canvas>
    </div>
  );
}

export default CharacterAnimation;
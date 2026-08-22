'use client';

import { useRef } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import { Icosahedron, Edges } from '@react-three/drei';
import * as THREE from 'three';

export default function Flourish3D({ reducedMotion }: { reducedMotion?: boolean }) {
  const meshRef = useRef<THREE.Mesh>(null);
  const { viewport } = useThree();

  useFrame((state, delta) => {
    if (!meshRef.current || reducedMotion) return;

    // Slow idle rotation (~20-30s per full turn)
    meshRef.current.rotation.y += delta * 0.25;
    meshRef.current.rotation.x += delta * 0.15;

    // Subtle tilt responsive to mouse (max ~8 degrees)
    const targetX = (state.pointer.x * viewport.width) / 10;
    const targetY = (state.pointer.y * viewport.height) / 10;
    
    // Lerp towards target to make it smooth
    meshRef.current.rotation.x = THREE.MathUtils.lerp(
      meshRef.current.rotation.x,
      targetY * 0.14, // ~8 degrees max
      0.1
    );
    meshRef.current.rotation.y = THREE.MathUtils.lerp(
      meshRef.current.rotation.y,
      targetX * 0.14,
      0.1
    );
  });

  return (
    <mesh ref={meshRef}>
      <Icosahedron args={[1.5, 0]}>
        <meshBasicMaterial color="#2B50E0" wireframe transparent opacity={0} />
        <Edges
          linewidth={1.5}
          threshold={15}
          color="#2B50E0"
        />
      </Icosahedron>
    </mesh>
  );
}

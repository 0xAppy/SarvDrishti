import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Sphere, Line, Text } from '@react-three/drei';

function MovingPacket({ start, end, color }) {
  const meshRef = useRef();
  
  useFrame(({ clock }) => {
    const t = (clock.getElapsedTime() * 0.5) % 1;
    if (meshRef.current) {
      meshRef.current.position.lerpVectors(start, end, t);
    }
  });

  return (
    <mesh ref={meshRef} position={start}>
      <sphereGeometry args={[0.08, 16, 16]} />
      <meshBasicMaterial color={color} />
    </mesh>
  );
}

function Node({ position, label, color }) {
  return (
    <group position={position}>
      <Sphere args={[0.2, 16, 16]}>
        <meshBasicMaterial color={color} wireframe />
      </Sphere>
      <Text position={[0, -0.4, 0]} fontSize={0.2} color="#a1a1aa" anchorX="center" anchorY="middle">
        {label}
      </Text>
    </group>
  );
}

export default function LogPipelineNetwork() {
  const nodes = {
    firewall: [-4, 1.2, 0],
    syslog: [-4, 0, 0],
    webapp: [-4, -1.2, 0],
    ingest: [-1.5, 0, 0],
    parser: [1, 0, 0],
    validator: [3.5, 0, 0],
    db: [6, 0, 0]
  };

  const connections = [
    [nodes.firewall, nodes.ingest],
    [nodes.syslog, nodes.ingest],
    [nodes.webapp, nodes.ingest],
    [nodes.ingest, nodes.parser],
    [nodes.parser, nodes.validator],
    [nodes.validator, nodes.db]
  ];

  return (
    <div className="w-full h-40 bg-darkBg rounded border border-darkBorder overflow-hidden">
      <Canvas camera={{ position: [1, 0, 6.5], fov: 45 }} gl={{ antialias: false, powerPreference: "low-power" }}>
        <ambientLight intensity={0.5} />
        
        {/* Nodes */}
        <Node position={nodes.firewall} label="Firewall" color="#0891b2" />
        <Node position={nodes.syslog} label="Syslog" color="#0891b2" />
        <Node position={nodes.webapp} label="Web App" color="#0891b2" />
        <Node position={nodes.ingest} label="Ingest" color="#0284c7" />
        <Node position={nodes.parser} label="Parser" color="#0284c7" />
        <Node position={nodes.validator} label="Validate" color="#0284c7" />
        <Node position={nodes.db} label="Storage" color="#059669" />

        {/* Lines */}
        {connections.map((c, i) => (
          <Line key={i} points={c} color="#27272a" lineWidth={1} />
        ))}

        {/* Packets */}
        <MovingPacket start={nodes.firewall} end={nodes.ingest} color="#0891b2" />
        <MovingPacket start={nodes.syslog} end={nodes.ingest} color="#0891b2" />
        <MovingPacket start={nodes.ingest} end={nodes.parser} color="#0284c7" />
        <MovingPacket start={nodes.parser} end={nodes.validator} color="#0284c7" />
        <MovingPacket start={nodes.validator} end={nodes.db} color="#059669" />
      </Canvas>
    </div>
  );
}

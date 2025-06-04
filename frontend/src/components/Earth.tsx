import React, { useEffect, useRef, useState } from 'react';
import Globe from 'react-globe.gl';
import type { GlobeMethods } from 'react-globe.gl';

export type Point = {
  lat: number;
  lng: number;
};

const Earth: React.FC = () => {
  const globeRef = useRef<GlobeMethods | undefined>(undefined);
  const [points, setPoints] = useState<Point[]>([]);

  useEffect(() => {
    if (globeRef.current) {
      const controls = globeRef.current.controls();
      controls.autoRotate = true;
      controls.autoRotateSpeed = 0.5;
    }
  }, []);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws");

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "init") {
        // Reçoit tous les points actuels à la connexion
        const points = data.markers.map((m:any) =>m.gps);
        //data.inner_weathers.map((iw: any) => iw.point);
        setPoints(points);
      } else {
        // Reçoit un nouveau point en temps réel
        setPoints(prev => [...prev, data]);
      }
    };

    socket.onclose = () => {
      console.log("WebSocket déconnecté");
    };

    return () => socket.close();
  }, []);

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <Globe
        ref={globeRef}
        globeImageUrl="//cdn.jsdelivr.net/npm/three-globe/example/img/earth-blue-marble.jpg"
        bumpImageUrl="//cdn.jsdelivr.net/npm/three-globe/example/img/earth-topology.png"
        pointsData={points}
        pointLat={(d) => (d as Point).lat}
        pointLng={(d) => (d as Point).lng}
        pointAltitude={0.1}
        pointColor={() => 'lightgreen'}
      />
    </div>
  );
};

export default Earth;
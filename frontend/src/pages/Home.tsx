import '../App.css';
import React from 'react';
import Earth from '../components/Earth';
import AddMarkerDrawer from './AddMarker'

const Home: React.FC = () => {
  return (
    <div id="canvas-container" style={{ position: "relative" }}>
      <Earth />
      <AddMarkerDrawer isOpen={false} onClose={() => {}} />
    </div>
  );
};

export default Home;
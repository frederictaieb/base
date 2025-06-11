import '../App.css';
import React from 'react';
import Earth from '../components/Earth';
import SendTextfile from './SendTextfile'

const Home: React.FC = () => {
  return (
    <div id="canvas-container" style={{ position: "relative" }}>
      <Earth />
      <SendTextfile isOpen={false} onClose={() => {}} />
    </div>
  );
};

export default Home;
import '../App.css';
import React from 'react';
import Earth from '../components/Earth';

const Home: React.FC = () => {
  return (
    <div>
      <div id="header">Welcome on the Earth</div>
      <div id="canvas-container">
        <Earth />
      </div>
    </div>
  );
};

export default Home;
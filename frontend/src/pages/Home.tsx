import '../App.css';
import React from 'react';
import Earth from '../components/Earth';

const Home: React.FC = () => {
  return (
      <div id="canvas-container">
        <Earth />
      </div>
  );
};

export default Home;
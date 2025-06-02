import './App.css';
import React from 'react';
import Earth from './components/Earth';

const App: React.FC = () => {
  return (
    <>
      <div id="header">Welcome on the Earth</div>
      <div id="canvas-container">
        <Earth />
      </div>
    </>
  );
};

export default App;
import React, { useRef, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import AddMarkerDrawer from "./pages/AddMarker";
import Navbar from "./components/Navbar";
import RadioPlayer from "./components/RadioPlayer";

const App: React.FC = () => {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [isMuted, setIsMuted] = useState(true); // Par défaut muté
  const audioRef = useRef<HTMLAudioElement>(null);

  // Fonction pour toggle le mute
  const toggleMute = () => {
    setIsMuted((prev) => {
      const newMuted = !prev;
      if (audioRef.current) {
        audioRef.current.muted = newMuted;
        // Si on unmute, il faut peut-être relancer la lecture (pour certains navigateurs)
        if (!newMuted) {
          audioRef.current.play().catch(() => {});
        }
      }
      return newMuted;
    });
  };

  return (
    <Router>
      <Navbar
        onOpenDrawer={() => setDrawerOpen(true)}
        isMuted={isMuted}
        onToggleMute={toggleMute}
      />
      <RadioPlayer audioRef={audioRef} />
      <AddMarkerDrawer isOpen={drawerOpen} onClose={() => setDrawerOpen(false)} />
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </Router>
  );
};

export default App;
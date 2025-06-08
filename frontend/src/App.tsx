import React, { useRef, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import AddMarkerDrawer from "./pages/AddMarker";
import Navbar from "./components/Navbar";
import RadioPlayer from "./components/RadioPlayer";
import TextFormPage from "./pages/text";

const App: React.FC = () => {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [isMuted, setIsMuted] = useState(true); // Par défaut muté
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const fadeDuration = 2400; // ms (4 secondes)
  const fadeSteps = 16;
  const [isFading, setIsFading] = useState(false);

  // Fade le volume de start à end
  const fadeVolume = (start: number, end: number, callback?: () => void) => {
    const audio = audioRef.current;
    if (!audio) return;
    setIsFading(true);
    const step = (end - start) / fadeSteps;
    let current = start;
    let count = 0;

    const fade = () => {
      if (!audio) return;
      current += step;
      count++;
      const min = Math.min(start, end);
      const max = Math.max(start, end);
      audio.volume = Math.max(min, Math.min(max, current));
      if ((step > 0 && current < end) || (step < 0 && current > end)) {
        setTimeout(fade, fadeDuration / fadeSteps);
      } else {
        audio.volume = Math.max(min, Math.min(max, end));
        setIsFading(false);
        if (callback) callback();
      }
    };

    fade();
  };

  // Fonction pour toggle le mute avec fade
  const toggleMute = () => {
    const audio = audioRef.current;
    if (!audio) return;
    if (isMuted) {
      // On change l'icône tout de suite
      setIsMuted(false);
      // Fade in
      audio.muted = false;
      audio.volume = 0;
      audio.play().catch(() => {});
      fadeVolume(0, 0.25);
    } else {
      // On change l'icône tout de suite

      // Fade out
      fadeVolume(audio.volume, 0, () => {
        audio.muted = true;
      });
      setIsMuted(true);
    }
  };

  return (
    <Router>
      <Navbar
        onOpenDrawer={() => setDrawerOpen(true)}
        isMuted={isMuted}
        onToggleMute={toggleMute}
        isFading={isFading}
      />
      <RadioPlayer audioRef={audioRef} />
      <AddMarkerDrawer isOpen={drawerOpen} onClose={() => setDrawerOpen(false)} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/text" element={<TextFormPage />} />
      </Routes>
    </Router>
  );
};

export default App;
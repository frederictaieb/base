import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import AddMarkerDrawer from "./pages/AddMarker";
import Navbar from "./components/Navbar";

const App: React.FC = () => {
  const [drawerOpen, setDrawerOpen] = useState(false);

  return (
    <Router>
      <Navbar onOpenDrawer={() => setDrawerOpen(true)} />
      <AddMarkerDrawer isOpen={drawerOpen} onClose={() => setDrawerOpen(false)} />
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </Router>
  );
};

export default App;
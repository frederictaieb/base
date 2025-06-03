import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import AddPoint from "./pages/AddPoint";
import Navbar from "./components/Navbar";
import "./styles/styles.css";

const App: React.FC = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/tools/add-point" element={<AddPoint />} />
      </Routes>
    </Router>
  );
};

export default App;
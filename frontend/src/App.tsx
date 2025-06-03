import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import AddInnerWeather from "./pages/AddInnerWeather";
import Navbar from "./components/Navbar";
import "./styles/styles.css";

const App: React.FC = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/tools/add-point" element={<AddInnerWeather />} />
      </Routes>
    </Router>
  );
};

export default App;
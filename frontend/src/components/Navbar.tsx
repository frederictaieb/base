import React from "react";
import { Link } from "react-router-dom";

const Navbar: React.FC = () => (
  <nav style={{
    width: "100vw",
    position: "fixed", // Pour qu'elle reste en haut même en scrollant
    top: 0,
    left: 0,
    zIndex: 1000,
    padding: "1rem",
    background: "black",
    color: "#fff",
    display: "flex",
    gap: "1rem",
    boxSizing: "border-box"
  }}>
    <Link to="/" style={{ color: "#fff", textDecoration: "none" }}>Home</Link>
    <Link to="/tools/add-point" style={{ color: "#fff", textDecoration: "none" }}>Add Point</Link>
  </nav>
);

export default Navbar;
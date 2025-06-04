import React from "react";

type NavbarProps = {
  onOpenDrawer: () => void;
};

const Navbar: React.FC<NavbarProps> = ({ onOpenDrawer }) => (
  <nav className="fixed top-0 left-0 w-full z-50 bg-black flex justify-end items-center px-6 py-3">
    <button
      onClick={onOpenDrawer}
      className="flex items-center justify-center w-10 h-10 rounded-full hover:bg-white/10 transition"
      aria-label="Open Add Marker"
    >
      {/* SVG: three dots in a circle, white */}
      <svg width="32" height="32" viewBox="0 0 36 36">
        <circle cx="18" cy="18" r="16" stroke="white" strokeWidth="1" fill="none"/>
        <circle cx="12" cy="18" r="1.5" fill="white"/>
        <circle cx="18" cy="18" r="1.5" fill="white"/>
        <circle cx="24" cy="18" r="1.5" fill="white"/>
      </svg>
    </button>
  </nav>
);

export default Navbar;
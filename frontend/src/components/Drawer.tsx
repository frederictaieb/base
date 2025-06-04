import React from "react";

type DrawerProps = {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
};

const Drawer: React.FC<DrawerProps> = ({ isOpen, onClose, children }) => (
  <div>
    {/* Overlay */}
    {isOpen && (
      <div
        className="fixed inset-0 bg-black/30 z-[1000]"
        onClick={onClose}
      />
    )}
    {/* Drawer panel */}
    <div
      className={`fixed top-0 right-0 h-screen w-[420px] bg-black shadow-2xl z-[1100] transform transition-transform duration-300 overflow-y-auto p-8 ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}
    >
      <button
        onClick={onClose}
        className="absolute top-4 right-4 text-white text-2xl hover:text-gray-300 focus:outline-none"
        aria-label="Close"
      >
        ×
      </button>
      {children}
    </div>
  </div>
);

export default Drawer;
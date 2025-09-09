import React from "react";
import "../styles/ScrollToBottom.css";

const ScrollToBottom = ({ onClick, visible }) => {
  if (!visible) return null;
  return (
    <button
      className="scroll-to-bottom-btn"
      onClick={onClick}
      aria-label="Scroll to bottom"
    >
      ↓
    </button>
  );
};

export default ScrollToBottom;

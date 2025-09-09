import React from "react";
import "../styles/LoadingIndicator.css";

const LoadingIndicator = () => (
  <div className="loading-indicator">
    <span className="spinner"></span> Generating response...
  </div>
);

export default LoadingIndicator;

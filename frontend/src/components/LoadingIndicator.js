import React from "react";
import "../styles/LoadingIndicator.css";

const LoadingIndicator = ({ loading }) => (
  <div className="loading-indicator-wrapper">
    {loading && (
      <div className="loading-indicator">
        <span className="spinner"></span> Generating response...
      </div>
    )}
  </div>
);

export default LoadingIndicator;

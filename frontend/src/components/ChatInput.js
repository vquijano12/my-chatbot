import React from "react";
import "../styles/ChatInput.css";

const ChatInput = ({
  input,
  handleInputChange,
  handleSubmit,
  textareaRef,
  loading,
}) => (
  <form onSubmit={handleSubmit}>
    <textarea
      ref={textareaRef}
      value={input}
      onChange={handleInputChange}
      rows={1}
      className="chat-input"
      style={{ resize: "none" }}
    />
    <button className="submit-button" type="submit" disabled={loading}>
      Send
    </button>
  </form>
);

export default ChatInput;

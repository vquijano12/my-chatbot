import React from "react";

const MessageBubble = ({ role, content }) => (
  <div className={role === "user" ? "user-row" : "assistant-row"}>
    <div className={role === "user" ? "user-message" : "assistant-message"}>
      <b>{role === "user" ? "You" : "Bot"}:</b> {content}
    </div>
  </div>
);

export default MessageBubble;

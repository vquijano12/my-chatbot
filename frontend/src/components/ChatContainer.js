import React from "react";
import MessageBubble from "./MessageBubble";

const ChatContainer = ({ messages, chatEndRef }) => (
  <div className="chat">
    {messages.map((msg, idx) => (
      <MessageBubble key={idx} role={msg.role} content={msg.content} />
    ))}
    <div ref={chatEndRef} />
  </div>
);

export default ChatContainer;

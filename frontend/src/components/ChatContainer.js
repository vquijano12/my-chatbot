import React from "react";
import MessageBubble from "./MessageBubble";
import ScrollToBottom from "./ScrollToBottom";
import "../styles/ChatContainer.css";

const ChatContainer = ({
  messages,
  chatEndRef,
  chatContainerRef,
  showScrollBtn,
  scrollToBottom,
}) => (
  <div className="chat" ref={chatContainerRef}>
    {messages.map((msg, idx) => (
      <MessageBubble key={idx} role={msg.role} content={msg.content} />
    ))}
    <div ref={chatEndRef} />
    <div className="scroll-to-bottom-wrapper">
      <ScrollToBottom onClick={scrollToBottom} visible={showScrollBtn} />
    </div>
  </div>
);

export default ChatContainer;
